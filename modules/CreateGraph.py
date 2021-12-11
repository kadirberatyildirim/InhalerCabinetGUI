
from matplotlib import pyplot as plt

def CreateTemperatureGraph(temperaturevalues):
    temperaturevalues = [x for x in temperaturevalues if x != -1]
    
    plt.plot(range(len(temperaturevalues)), temperaturevalues, label='Temperature Values')
    plt.xlabel('Zaman (sn)')
    plt.ylabel('Sıcaklık')
    plt.show()
        
def CreateOxyGraph(oxyvalues):
    oxyvalues = [x for x in oxyvalues if x != -1]
    
    plt.plot(range(len(oxyvalues)), oxyvalues, label='Oxygen Values')
    plt.xlabel('Zaman (sn)')
    plt.ylabel('Oksijen Yüzdesi')
    plt.show()

def CreateCOGraph(covalues):
    covalues = [x for x in covalues if x != -1]
		
    plt.plot(range(len(covalues)), covalues, label='CO Values')
    plt.xlabel('Zaman (sn)')
    plt.ylabel('Karbonmonoksit Yüzdesi')
    plt.show()
		
def CreateHumidityGraph(humidityvalues):
    humidityvalues = [x for x in humidityvalues if x != -1]
		
    plt.plot(range(len(humidityvalues)), humidityvalues, label='Humidity Values')
    plt.xlabel('Zaman (sn)')
    plt.ylabel('Nem Yüzdesi')
    plt.show()

def CreateCO2Graph(co2values):
    co2values = [x for x in co2values if x != -1]
		
    plt.plot(range(len(co2values)), co2values, label='CO2 Values')
    plt.xlabel('Zaman (sn)')
    plt.ylabel('Karbondioksit Yüzdesi')
    plt.show()
