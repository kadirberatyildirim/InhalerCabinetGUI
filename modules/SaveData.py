
import csv

def SaveasCSV(header, temperature, humidity, o2, co, co2, path):
		fieldnames = ['Sicaklik', 'Nem', 'Oksijen Yüzdesi', 'Karbonmonoksit Yüzdesi', 'Karbondioksit Yüzdesi']
		with open (path + '.csv', 'w', newline='') as myfile:
			wr = csv.writer(myfile)
			wr.writerow(fieldnames)
			for i in range(0, len(temperature)):
				temporaryValuesList = [temperature[i], humidity[i], o2[i], co[i], co2[i]]
				wr.writerow(temporaryValuesList)

def SaveasPDF(header, temperature, humidity, o2, co, co2):
	return
