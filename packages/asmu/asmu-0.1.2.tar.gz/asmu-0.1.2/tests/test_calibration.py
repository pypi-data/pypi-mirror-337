"""test_gainramp.py
PyTest for the calibration analyzers CalIInput and CalIOutput.
"""
import numpy as np
import asmu

def test_caliinput(benchmark):
    Vp = 1
    outgain = 0.1
    # create objects
    interface = asmu.Interface(samplerate=44100,
                               blocksize=8192,
                               analog_output_channels=[1],
                               analog_input_channels=[1],
                               no_audio_device = True)
    sine = asmu.generator.Sine(interface, 1000)
    gain05 = asmu.effect.Gain(interface, 0.5)
    caliinput = asmu.analyzer.CalIInput(interface, Vp, "V")
    calioutput = asmu.analyzer.CalIOutput(interface, outgain, "V", interface.ioutput())

    # establish connections
    sine.output().connect(gain05.input())
    gain05.output().connect(caliinput.input())
    gain05.output().connect(calioutput.input())

    # create dummy array(s) for callback
    data = np.empty((interface.blocksize, 1), dtype = np.float32)
    # repeatedly call callback
    while not caliinput.finished(block = False):
        interface.callback(data, data, None, None, None)

    fV, cV = caliinput.evaluate(iinput=interface.iinput())
    # we used a sine with arbitrary amplitude 0.5 as our generated input signal, and a calibration value of 1Vp.
    # So to get from arbitrary to input voltage, cV should be 2.
    # The values are not perfect due to the limited window size.
    print(f"IInput: fV = {fV:.2f}Hz, cV = {cV:.2f}")
    assert abs(fV-1000) < 5, "Frequency deviates more than allowed range."
    assert abs(cV - Vp/0.5) < Vp/0.5*0.1, "Amplitude deviates more than allowed range."
    # check if calibration values were correctly written to IInput
    assert fV == interface.iinput().fV
    assert cV == interface.iinput().cV

    fV, cV = calioutput.evaluate(iinput = interface.iinput())
    # we theoretically generated a sine with arbitrary amplitude 0.1 and recieved a sine with a voltage amplitude of 1Vp.
    # So to get from voltage to the arbitrary amplitude used by the interface, 1/cV should be 0.1, so cV should be 10.
    # The values are not perfect due to the limited window size.
    print(f"IOutput: fV = {fV:.2f}Hz, cV = {cV:.2f}")
    assert abs(fV-1000) < 5, "Frequency deviates more than allowed range."
    assert abs(cV - Vp/outgain) < Vp/outgain*0.1, "Amplitude deviates more than allowed range."
    # check if calibration values were correctly written to IOutput
    assert fV == interface.ioutput().fV
    assert cV == interface.ioutput().cV

    # benchmark (calls callback very often)
    caliinput.restart()
    calioutput.restart()
    benchmark(interface.callback, data, data, None, None, None)


if __name__ == "__main__":
    test_caliinput(lambda x, *args: [x(*args) for _ in range(100)][0])
