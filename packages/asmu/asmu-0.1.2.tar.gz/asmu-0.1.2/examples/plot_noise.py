"""Simple program to test and visualize the ramp produced by the GainRamp effect."""
import numpy as np
import matplotlib.pyplot as plt
import asmu

def plot_gainramp():
    # create objects
    interface = asmu.Interface(samplerate=44100,
                               blocksize=1024,
                               analog_output_channels=[1, 2],
                               no_audio_device = True)
    wn = asmu.generator.Noise(interface, weight = "white")
    pn = asmu.generator.Noise(interface, weight = "pink")

    # establish connections
    wn.output().connect(interface.ioutput(ch=1))
    pn.output().connect(interface.ioutput(ch=2))

    # inti plot
    fig, axs = plt.subplots(2)

    # setup vectors
    outdata = np.empty((interface.blocksize, 2), dtype=np.float32)
    x = np.linspace(0, 1, interface.blocksize)

    # run callback loop
    pn_avgs = []
    wn_avgs = []
    for i in range(100):
        interface.callback(None, outdata, None, None, None)
        wn_avgs.append(np.abs(np.fft.rfft(outdata[:, 0], norm="forward"))*2)
        pn_avgs.append(np.abs(np.fft.rfft(outdata[:, 1], norm="forward"))*2)

    axs[0].plot(outdata[:, 0], label=f"weight = \"white\"")
    axs[0].plot(outdata[:, 1], label=f"weight = \"pink\"")
    wn_spec = np.mean(wn_avgs, axis=0)
    pn_spec = np.mean(pn_avgs, axis=0)
    axs[1].plot(np.fft.rfftfreq(interface.blocksize, 1/interface.samplerate), wn_spec, label=f"weight = \"white\"")
    axs[1].plot(np.fft.rfftfreq(interface.blocksize, 1/interface.samplerate), pn_spec, label=f"weight = \"pink\"")

    # setup plot and show
    axs[0].set(title="Noise and Spectrum (100 averages)", xlabel="time in seconds", ylabel="value")
    axs[1].set(xlabel="frequency in Hz", ylabel="magnitude")
    for ax in axs:
        ax.grid()
        ax.legend()

    fig.tight_layout()
    # Uncomment this if you dont want to save the plot
    # fig.savefig("docs/imgs/plot_noise.png", dpi=300)

    plt.show()

if __name__ == "__main__":
    plot_gainramp()
