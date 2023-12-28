## Hakkında :
#### Bu basit Python uygulaması, bir istemci-sunucu mimarisi kullanarak sohbet etmeyi sağlar. İstemciler, sunucuya bağlanarak birbirlerine mesaj gönderebilirler.<br><br><br>

## Uygulama Nasıl Çalışır? :
### Sunucu :
#### Sunucu, istemcilerin bağlanmasını dinleyen bir soket oluşturur ve belirli bir portu bekler. İstemciler bağlandığında, her biri için ayrı bir iş parçacığı başlatılır ve iletişim sağlanır. İstemci bağlantıları takip edilir ve bağlantı durumları güncellenir. Kullanıcı adı ve mesajları işleyerek istemciler arasında iletişim kurar.<br>

### İstemci :
#### Kullanıcıdan bir kullanıcı adı alır ve sunucuya bağlanır.İki iş parçacığı başlatılır: biri kullanıcının mesajlarını dinler, diğeri kullanıcıdan mesajları alır ve sunucuya iletiler. Kullanıcı, "disconnect" yazarak sunucudan çıkabilir veya diğer kullanıcılara özel mesajlar gönderebilir.<br><br><br>

## Özellikler :
    1-) İstemciler arası özel mesajlaşma yapılabilir.
    2-) Kullanıcı adları ve bağlantı durumları takip edilir.
    3-) "disconnect" komutu ile güvenli bir şekilde sunucudan çıkış yapılabilir.
    4-) Hata durumları ve güvenlik kontrolü için gerekli kontroller eklenmiştir.



## Kullanım :
    1-) "server.py" dosyasını çalıştırarak sunucuyu başlatın.
    2-) "client.py" dosyasını çalıştırarak istemciyi başlatın.
    3-) Kullanıcı adı belirtin.
    4-) İstemci arayüzünde diğer kullanıcılara genel veya özel mesajlar gönderebilirsiniz.
