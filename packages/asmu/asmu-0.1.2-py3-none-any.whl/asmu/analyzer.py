"""In this submodule you can find all analyzers, so "audio processors" with one or multiple inputs."""
import threading
from typing import TYPE_CHECKING, Literal, Union, Tuple
import numpy as np
from .acore import AAnalyzer
from .processor import Analyzer
from .io import Input

if TYPE_CHECKING:
    from .io import IInput, IOutput
    from .afile import AFile
    from .interface import Interface
    from .types import AData, FFTData


class Recorder(Analyzer):
    def __init__(self, interface: "Interface", afile: "AFile") -> None:
        """The Recorder class analyzer is used to record audio to a given file.
        It is a multi input analyzer, with the input count extracted from the given AFile.
        Input-update is not supported.

        Args:
            interface: Reference to an Interface instance.
            afile: Reference to an AFile instance.

        Raises:
            ValueError: The given AFile was not opened.
        """
        # check afile is open and reset
        self._afile = afile
        if afile.closed:
            raise ValueError("The given AFile was not opened.")
        afile.flush()
        afile.seek(0)

        arecorder = self._ARecorder(afile, interface.blocksize, interface.start_frame)
        super().__init__(aanalyzer = arecorder,
                         interface = interface,
                         inputs = tuple(Input(self) for i in range(afile.channels)),
                         in_update = False)

    class _ARecorder(AAnalyzer):
        def __init__(self, afile: "AFile", blocksize, start_frame) -> None:
            self._afile = afile
            super().__init__(in_buffer = True,
                             blocksize = blocksize,
                             start_frame = start_frame)

        def _process(self) -> None:
            self._afile.write(self._in_buf)


class _CalIO(AAnalyzer):
        def __init__(self, averages: int, blocksize: int, start_frame: int) -> None:
            self.finished_event = threading.Event()

            # result averaging
            self._avgs = averages + 3 # we dont consider the first three measurements
            self.counter = 0
            self.us = np.zeros(self._avgs, dtype=np.float32)
            self.ks = np.zeros(self._avgs, dtype=np.float32)

            # arrays needed for the array processing
            self._fft = np.empty(int(blocksize/2+1), dtype=np.complex64)
            self._spectrum = np.empty(int(blocksize/2+1), dtype=np.float32)
            self._window = np.hanning(blocksize)
            super().__init__(in_buffer = True,
                             blocksize = blocksize,
                             start_frame = start_frame)

        def _process(self) -> None:
            if self.finished_event.is_set():
                return
            if self.counter < self._avgs:
                self.physical_fft(self._in_buf[:, 0], self._fft, window = self._window)
                np.abs(self._fft, out = self._spectrum)

                kmax = np.argmax(self._spectrum)
                self.ks[self.counter] = kmax
                self.us[self.counter] = self._spectrum[kmax]
                self.counter += 1
            elif not self.finished_event.is_set():
                self.finished_event.set()

        def physical_fft(self, indata: "AData", outdata: "FFTData", window: "AData" = 1) -> None:
            np.fft.rfft(indata*window, norm = "forward", out = outdata)
            outdata[:] *= 2/np.mean(window)


class CalIInput(Analyzer):
    def __init__(self, interface: "Interface", value: float, unit: Literal["V", "Pa", "SPL"], gain: float = 0, averages: int = 100) -> None:
        """The CalcIInput class analyzer is used to calibrate the connected interface IInput.
        It is a single input analyzer, therefore input-update is not supported.

        Args:
            interface: Reference to an Interface instance.
            value: The value of the signal used for calibration.
            unit: The unit of the value given

                - `"V"`   : Peak amplitude of the sinusoidal signal in Volt.
                - `"Pa"`  : Peak amplitude of the sinusoidal signal in Pascal.
                - `"SPL"` : Sound Pressure Level (RMS pressure in Dezibel).

            gain: Gain setting of the interface. This is not used for the calculation, but stored in the IInput.
            averages: How many averages should be calcualted.
        """
        self._value = value
        self._unit = unit
        self._gain = gain

        self._calio = _CalIO(averages, interface.blocksize, interface.start_frame)
        super().__init__(aanalyzer = self._calio,
                         interface = interface,
                         inputs = (Input(self), ),
                         in_update = False)

    def evaluate(self, save: bool = True, iinput: "IInput" = None) -> Union[Tuple[float, float], False]:
        """If the measurement is finished, this evaluates the result and returns True.
        If the measurement is still running, False is returned.

        Args:
            save: Decides if the results should be daved to the connected or given IInput.
            iinput: The IInput to save the calibration to.

        Returns:
            (Frequency, Calibration Factor), when everything was successful. `False`, when the measurement is not done yet.

        Raises:
            ValueError: Given Unit is unknown.
        """
        if not self.finished(block = False):
            return False
        # calculate peak amplitude
        if self._unit == "V" or self._unit == "Pa":
            peak = self._value
        elif self._unit == "SPL":
            peak = 2e-5 * 10 ** (self._value / 20) * np.sqrt(2)
        else:
            raise ValueError("Given Unit is unknown.")
        # calculate calibration factor and frquency
        c = peak/np.mean(self._calio.us[2:])
        fs = np.fft.rfftfreq(self._interface.blocksize, 1/self._interface.samplerate)
        f = np.interp(np.mean(self._calio.ks[2:]), np.arange(fs.size), fs)
        # get iinput if given
        if iinput is None:
            iinput = self._inputs[0].connected_output
        # write to IInput
        if save:
            iinput.gain = self._gain
            if self._unit == "V":
                iinput.cV = c
                iinput.fV = f
            elif self._unit == "SPL" or self._unit == "Pa":
                iinput.cPa = c
                iinput.fPa = f
        return (f, c)
        
    def finished(self, block: bool = True, timeout: float = 1) -> bool:
        """This function can be used to wait for the calibration to be done.
        
        Args:
            block: Decides if the call of finished() should block.
            timeout: The timeout after which False is returned.

        Returns:
            `True`, when the calibration finished. `False` on timeout.
        """
        if block:
            return self._calio.finished_event.wait(timeout = timeout)
        else:
            return self._calio.finished_event.is_set()

    def restart(self) -> bool:
        """Restart the calibration, unset the finished() flag.
        If the audio stream is still running, it starts with the next measurement series right away.
        
        Returns:
            `True`, when successful. `False`, when the calibration isn't finished yet."""
        if not self.finished(block=False):
            return False
        self._calio.counter = 0
        self._calio.finished_event.clear()
        return True


class CalIOutput(Analyzer):
    def __init__(self, interface: "Interface", value: float, unit: Literal["V", "Pa"], ioutput: "IOutput", gain: float = 0, averages: int = 100) -> None:
        """The CalcIOutput class analyzer is used to calibrate the given IOutput.
        For this calibration procedure a Sine generator with an amplitude of value has to be connected to the given IOutput.
        This IOutput must be physically connected to the IInput, which needs to be pre-calibrated, 
        and this IInput must be connected to this analyzer.
        It is a single input analyzer, therefore input-update is not supported.

        Args:
            interface: Reference to an Interface instance.
            value: The peak amplitude value of the signal used for calibration in arbitrary units.
            unit: The physical quantity to calibrate for.
            ioutput: The IOutput that is used to generate the signal and connected to the IInput.
            gain: Gain setting of the interface. This is not used for the calculation, but stored in the IOutput.
            averages: How many averages should be calcualted.
        """
        self._value = value
        self._unit = unit
        self._ioutput = ioutput
        self._gain = gain

        self._calio = _CalIO(averages, interface.blocksize, interface.start_frame)
        super().__init__(aanalyzer = self._calio,
                         interface = interface,
                         inputs = (Input(self), ),
                         in_update = False)

    def evaluate(self, save: bool = True, ioutput: "IOutput" = None, iinput: "IInput" = None) -> Union[Tuple[float, float], False]:
        """If the measurement is finished, this evaluates the result and returns True.
        If the measurement is still running, False is returned.

        Args:
            save: Decides if the results should be saved to the given IOutput.
            ioutput: The IOutput to save the calibration to.
            iinput: The IInput the analyzer is connected to. (Typically selected automatically)

        Returns:
            (Frequency, Calibration Factor), when everything was successful. `False`, when the measurement is not done yet.

        Raises:
            ValueError: Given Unit is unknown.
        """
        if not self.finished(block = False):
            return False
        # get iinput if not given
        if iinput is None:
            iinput = self._inputs[0].connected_output
        # get the measured value
        if self._unit == "V":
            peak = np.mean(self._calio.us[2:]) * iinput.cV
        elif self._unit == "Pa":
            peak = np.mean(self._calio.us[2:]) * iinput.cPa
        else:
            raise ValueError("Given Unit is unknown.")
        # calculate calibration factor and frquency
        c = peak/self._value
        fs = np.fft.rfftfreq(self._interface.blocksize, 1/self._interface.samplerate)
        f = np.interp(np.mean(self._calio.ks[2:]), np.arange(fs.size), fs)
        # get ioutput if not given
        if ioutput is None:
            ioutput = self._ioutput
        # write to IOutput
        if save:
            ioutput.gain = self._gain
            if self._unit == "V":
                ioutput.cV = c
                ioutput.fV = f
            elif self._unit == "Pa":
                ioutput.cPa = c
                ioutput.fPa = f
        return (f, c)

    def finished(self, block: bool = True, timeout: float = 1) -> bool:
        """This function can be used to wait for the calibration to be done.
        
        Args:
            block: Decides if the call of finished() should block.
            timeout: The timeout after which False is returned.

        Returns:
            `True` when the calibration finished. `False` on timeout.
        """
        if block:
            return self._calio.finished_event.wait(timeout = timeout)
        else:
            return self._calio.finished_event.is_set()

    def restart(self) -> bool:
        """Restart the calibration, unset the finished() flag.
        If the audio stream is still running, it starts with the next measurement series right away.
        
        Returns:
            `True` when successful. `False`, when the calibration isn't finished yet."""
        if not self.finished(block=False):
            return False
        self._calio.counter = 0
        self._calio.finished_event.clear()
        return True
