# Instagram Scraper

## Kurulum

1. **PostgreSQL Ayarları**:

   Komut satırını yönetici olarak çalıştırarak PostgreSQL'e bağlantı gerçekleştirin ve `iginfluencer` isminde bir Superuser ve `iginfluencer` isminde bir Database oluşturun.

   ```bash
   psql -U postgres
   CREATE USER iginfluencer WITH SUPERUSER PASSWORD 'iginfluencer';
   CREATE DATABASE iginfluencer;

2. **Gerekli Paketlerin Yüklenmesi**:

Gerekli paketleri yüklemek için terminalde aşağıdaki komutu çalıştırın:

bash
pip install -r requirements.txt
Veritabanı Yapısını Oluşturma:

3. **Veritabanı yapısını oluşturmak için aşağıdaki komutları sırayla çalıştırın**:

bash
python manage.py makemigrations ig_scraper
python manage.py migrate

4. **Sunucuyu Başlatma**:

Sunucuyu başlatmak için aşağıdaki komutu kullanın:

bash
python manage.py runserver 80

5. **Celery Görevlerini Başlatma**:

Veritabanı yapısını oluşturmak için aşağıdaki komutları kullanın:

bash
python manage.py makemigrations django_celery_beat 
python manage.py migrate django_celery_beat 
python manage.py makemigrations django_celery_results 
python manage.py migrate django_celery_results 

Komut satırını yönetici olarak çalıştırarak Redis server'ını ayağa kaldırın:

bash
redis-server

Terminal üzerinden aşağıdaki komutları çalıştırın:

bash
celery -A ig_scraper worker --loglevel=info --pool=solo
celery -A ig_scraper beat -l info


## Kullanım

#### 1-) Influencer Yönetimi:

http://127.0.0.1/influencers/ adresine giderek influencer ekleme/silme işlemlerini gerçekleştirebilirsiniz.

#### 2-) Superuser Oluşturma:

Terminalde aşağıdaki komutu çalıştırarak bir superuser tanımlayabilirsiniz:

bash
python manage.py createsuperuser 

#### 3-) Admin Paneli:

http://127.0.0.1/admin/ adresine tanımladığınız superuser ile giriş yaparak Influencer, Post ve Story tabloları üzerinde işlemler yapabilirsiniz.

#### 4-) Veri Yönetimi:

Eklediğiniz her bir influencer'ın post ve story verileri AWS S3'e otomatik olarak indirilecek ve web sayfasında bu kaynaktan görseller gösterilecektir.

#### 5-) Influencer Sınırı:

En fazla 20 influencer ekleyebilirsiniz.

#### 6-) Celery Görevleri:

Celery komutlarını çalıştırdığınızda eklenmiş olan influencer'ların post ve story verileri her saat başı güncellenerek detay sayfalarında gösterilir.

### App Dosyaları
#### ig_scraper/admin.py: 
Influencer, Post ve Story modellerinin admin paneli bağlantılarının bulunduğu dosya.

#### ig_scraper/forms.py: 
Influencer ekleme işlemini gerçekleştirme arayüzü olarak form yapısının tanımlandığı dosya.

#### ig_scraper/models.py: 
Influencer, Post ve Story tablolarının tanımlandığı dosya.

#### ig_scraper/scraper.py: 
Instagram scraping işlemlerini içeren dosya. Instaloader ile login ve veri çekme işlemleri ve çekilen verilerin AWS S3 depolama alanına indirilmesi işlemleri burada tanımlanmıştır.

#### ig_scraper/tasks.py: 
Periyodik görev fonksiyonunun tanımlı olduğu dosya.

#### ig_scraper/tests.py: 
Influencer, Post ve Story nesnelerinin CRUD işlemlerini, template dosyalarının çalışmasını ve fonksiyonların çalışma süreçlerini test eden fonksiyonları içeren dosya.
#### ig_scraper/urls.py: 
List, add, delete ve detail sayfalarının URL'lerini içeren dosya.
#### ig_scraper/views.py:
 Influencer, Post ve Story nesnelerinin CRUD işlemlerinin tanımlandığı dosya.