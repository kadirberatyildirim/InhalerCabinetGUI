
from matplotlib import pyplot as plt

def CreateTemperatureGraph(temperaturevalues):
		x_axis = []
		for i in range(0, len(temperaturevalues)):
			x_axis.append(i)
		plt.plot(x_axis, temperaturevalues, label='Temperature Values')
		plt.xlabel('Zaman (sn)')
		plt.ylabel('Sıcaklık')
		plt.show()

def CreateOxyGraph(oxyvalues):
		x_axis = []
		for i in range(0, len(oxyvalues)):
			x_axis.append(i)
		plt.plot(x_axis, oxyvalues, label='Oxygen Values')
		plt.xlabel('Zaman (sn)')
		plt.ylabel('Oksijen Yüzdesi')
		plt.show()

def CreateCOGraph(covalues):
		x_axis = []
		for i in range(0, len(covalues)):
			x_axis.append(i)
		plt.plot(x_axis, covalues, label='CO Values')
		plt.xlabel('Zaman (sn)')
		plt.ylabel('Karbonmonoksit Yüzdesi')
		plt.show()
		
def CreateHumidityGraph(humidityvalues):
		x_axis = []
		for i in range(0, len(humidityvalues)):
			x_axis.append(i)
		plt.plot(x_axis, humidityvalues, label='Humidity Values')
		plt.xlabel('Zaman (sn)')
		plt.ylabel('Nem Yüzdesi')
		plt.show()
        
def CreateCO2Graph(co2values):
		x_axis = []
		for i in range(0, len(co2values)):
			x_axis.append(i)
		plt.plot(x_axis, co2values, label='CO2 Values')
		plt.xlabel('Zaman (sn)')
		plt.ylabel('Karbondioksit Yüzdesi')
		plt.show()
