import flask
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.io import hplot
from waveforms import sine_wave, square_wave, triangle_wave, sawtooth_wave, full_rectified_sine, half_rectified_sine
import numpy as np
import pyaudio

app = flask.Flask(__name__)

waves = {
    'sine': sine_wave,
    'square':   square_wave,
    'triangle': triangle_wave,
    'sawtooth':  sawtooth_wave,
    'full_rec': full_rectified_sine,
    "half_rec": half_rectified_sine
}

def getitem(obj, item, default):
    """
    Retrieve items from form
    """
    if item not in obj:
        return default
    else:
        return obj[item]

def tones(wave_form, frequency, terms):
    """
    Generate a tone from the Fourier Series waveforms
    """
    p = pyaudio.PyAudio()
    volume = 0.5     # range [0.0, 1.0]
    fs = 44100       # sampling rate, Hz, must be integer
    duration = 3.0
    samples = wave_form(np.arange(fs*duration),
                                  float(frequency)/fs,
                                  terms)[0].astype(np.float32)
    stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)
    stream.write(volume*samples)
    stream.stop_stream()
    stream.close()

    p.terminate()

@app.route("/")
def fourier_series():
    """
    Select waveform, frequency, and terms in a Fourier Series
    Display time and frequency domain plots and generate a tone
    """
    # This is automated by the button
    args = flask.request.args
    # Parameters for audio and plotting
    wave = waves[getitem(args, 'wave', 'sine')]
    frequency = int(getitem(args, 'frequency', 50))
    terms = int(getitem(args, 'terms', 10))
    # plot versus time t, 1000 data points, two periods
    t = np.linspace(0, 2.0/frequency, 1000)
    y, fre, amp = wave(t, frequency, terms)

    # Bokeh plotting
    TOOLS = "resize,wheel_zoom,reset,pan"
    s1 = figure(width=500, height=500, title=None, tools=TOOLS)
    s1.line(t, y)
    s1.xaxis.axis_label = "Time [seconds]"
    # 'Bar' plot created with boxes via the 'quad' method
    s2 = figure(width=500, height=500, tools=TOOLS, y_axis_type="log",
                y_range=(10**-4, 10**0), x_range=(0, fre.max()+10))
    s2.quad(
        bottom=0, top=amp,
        left=fre-1, right=fre+1)
    s2.xaxis.bounds = (0, fre.max()+10)
    s2.xaxis.axis_label = "Frequency [Hertz]"
    s2.ygrid.minor_grid_line_color = 'navy'
    s2.ygrid.minor_grid_line_alpha = 0.1
    fig = hplot(s1, s2)

    # Configure resources to include BokehJS inline in the document.
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(fig, INLINE)
    html = flask.render_template(
        'embed.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        wave=wave,
        frequency=frequency,
        terms=terms
    )

    return encode_utf8(html), tones(wave, frequency, terms)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
