
from matplotlib import pyplot as plt

def CreateTemperatureGraph(temperaturevalues):
    x_axis = [range(0, len(temperaturevalues), 5)]
    
    for i in range(len(temperaturevalues)):
        if temperaturevalues[i] == -1:
            del temperaturevalues[i]
            del x_axis[i]
    
    plt.plot(x_axis, temperaturevalues, label='Temperature Values')
    plt.xlabel('Zaman (sn)')
    plt.ylabel('Sıcaklık')
    
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    plt.show()
        
def CreateOxyGraph(oxyvalues):
    x_axis = [range(0, len(oxyvalues), 5)]
    
    for i in range(len(oxyvalues)):
        if oxyvalues[i] == -1:
            del oxyvalues[i]
            del x_axis[i]
    
    plt.plot(x_axis, oxyvalues, label='Oxygen Values')
    plt.xlabel('Zaman (sn)')
    plt.ylabel('Oksijen Yüzdesi')
    
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    plt.show()

def CreateCOGraph(covalues):
    x_axis = [range(0, len(covalues), 5)]
    
    for i in range(len(covalues)):
        if covalues[i] == -1:
            del covalues[i]
            del x_axis[i]
		
    plt.plot(x_axis, covalues, label='CO Values')
    plt.xlabel('Zaman (sn)')
    plt.ylabel('Karbonmonoksit Yüzdesi')
    
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    plt.show()
		
def CreateHumidityGraph(humidityvalues):
    x_axis = [range(0, len(humidityvalues), 5)]
    
    for i in range(len(humidityvalues)):
        if humidityvalues[i] == -1:
            del humidityvalues[i]
            del x_axis[i]
		
    plt.plot(x_axis, humidityvalues, label='Humidity Values')
    plt.xlabel('Zaman (sn)')
    plt.ylabel('Nem Yüzdesi')
    
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    plt.show()

def CreateCO2Graph(co2values):
    x_axis = [range(0, len(co2values), 5)]
    
    for i in range(len(co2values)):
        if co2values[i] == -1:
            del co2values[i]
            del x_axis[i]
		
    plt.plot(x_axis, co2values, label='CO2 Values')
    plt.xlabel('Zaman (sn)')
    plt.ylabel('Karbondioksit Yüzdesi')
    
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    plt.show()
