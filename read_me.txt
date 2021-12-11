
-------------About the code--------------

=====Arduino shorcuts
kabin içindeki havanın tahliye edilmesi için "z".
sigara kabini içindedi havanın tahiye edilmesi için "x".******deprecated********
sensörlerden veri istemek için "s". *********deprecated******
iqos içme ayarlarını seçmek için "q".
normal sigara içme ayarlarını seçmek için "c".
sigara içmeye başlama için "r".
sigara içmeyi duraklatmak için "p".
deneyi başlatmak için "d".
herşeyi durdurmak için "a".
sistemi kapanmadan önce "e".
sigara tutucu (holder) ' ın sıfır konumunu sıfırlama "f".
holder'ı çıkart "j".
kaç sigara içileceği ayarı "y" + str(number) 
deney süresi "h" + str(time) 

=====LCD monitör verileri nasıl okunuyor ?
Arduino belirli aralıklar ile buffer'a sensör verilerini yazıyor
mainwindow.py de açılan bir QTimer objesi her saniye buffer'ı kontrol ediyor
Eğer ser.in_waiting 0'dan farklı ise okumayı gerçekleştiriyor
!!!Dikkat!!! buffer'a sadece sensör verilerinin girildiği varsayılmıştır!
v1.6.3'te 5 veri girdisi bulunmakta, sonradan CO monitörü alınınca onunda eklenmesi beklenmektedir.
Kodu güncelleyip indexleri ayarlamayı unutma!

=====Kodun çalışması için gerekli izinler
Eğer arduino port'u için chmod 777 komutu yapılmışsa, kod normal kullanıcı için de çalışır haldedir, yapılmadıysa root izni gerekir
Eğer port değişiyorsa, kodun içinde __init__ teki os.system kodunu ve openArduinoPort içindeki path'i değişmeyi unutma!

-------------There is an error ?--------------

=====LCD Monitors not displaying any sensor values
Do not forget that permission error is passed in try/except when trying to open the port of arduino!!!
If you do not see any values on LCD monitors, this probably is the reason!!!
For permission error: sudo chmod 777 /dev/ttyACM0 
change /dev/ttyACM0 to the actual path of arduino

Other reason may be that the code cannot open the port. If this is the case, check the path of the code!
To check arduino port on linux, in terminal : ls /dev/tty*
Do that with and without arduino connected via serial, that way, difference is arduino path.

******Yet another reason can be in .write command of serial library, inside readFromArduino method of mainwindow.py
Check that you are sending the signal correctly. It should be send in binary string.
Default (decided by our lazy member Ömer Faruk Kadi) is string s.
The write command should then go as : self.ser.write(b's \n')******deprecated******** 
Since v1.7, values are sent by arduino to buffer, then mainwindow.py checks if there is anything inside buffer.

After self.ser.readline(), output should be decoded to normal string and then should be splitted (data is in form 1/2/3/4...)
In main window code, this is done as follows: sensorData = self.ser.readline().decode('ascii')[:-2].split('/')
Then make sure to turn resulting list into a integer list, as it is created as a string list.
Integers 0, 1, 2, 3, 4 correspond to temperature, oxygen, carbon monoxide, humidity and carbon dioxide values respectively.
While writing numbers to LCD monitors, do not forget to use correct indexing!!

None of these worked ? Pray to god...

=====Kontrol tuşları çalışmıyor
Arduino'ya yollanan sinyallerin doğru olup olmadığını hem mainwindow.py kodunda, hem arduino kodunda kontrol et.
Yukarıda tüm komutlar yazılmış durumda.

