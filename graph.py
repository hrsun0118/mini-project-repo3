import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import matplotlib.dates as mdates

def build_graph(humidity_sensors, temperature_sensors):
    img = io.BytesIO()
    if len(humidity_sensors) == 0:
        plt.subplot(2,1,1)
        plt.title("No Humidity Data Available")
    else:
        for i in range(0,len(humidity_sensors)):
            # generate synthetic sensor readings
            plt.subplot(2,1,1)
            sensor_data_x = np.arange(0,100)
            sensor_data_y = [10+np.random.normal(0,10) for i in range(0,100)]
            plt.plot(sensor_data_x, sensor_data_y, label=humidity_sensors[i])
            plt.title("Streaming Humidity Data")
            plt.legend()
    if len(temperature_sensors) == 0:
        plt.subplot(2,1,2)
        plt.title("No Temperature Data Available")
    else:
        for i in range(0,len(temperature_sensors)):
            # generate synthetic sensor readings
            plt.subplot(2,1,2)
            sensor_data_x = np.arange(0,100)
            sensor_data_y = [10+np.random.normal(0,10) for i in range(0,100)]
            plt.plot(sensor_data_x, sensor_data_y, label=temperature_sensors[i])
            plt.title("Streaming Temperature Data")
            plt.legend()
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.subplots_adjust(hspace = 0.5)
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)