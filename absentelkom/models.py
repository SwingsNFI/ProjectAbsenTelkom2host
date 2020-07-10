from django.db import models
from django.utils import timezone

# Create your models here.
class Tbl_kelas(models.Model):
    id_kelas = models.CharField(primary_key=True, max_length=5)
    nama_kelas = models.CharField(max_length=9)

    class Meta:
        db_table = "tbl_kelas"

class Tbl_siswa(models.Model):
    id_siswa = models.CharField(primary_key=True, max_length=9)
    id_kelas = models.ForeignKey(Tbl_kelas, on_delete=models.CASCADE, max_length=5)
    nama_siswa = models.CharField(max_length=50)
    email_siswa = models.CharField(max_length=50)
    password_siswa = models.CharField(max_length=33)

    class Meta:
        db_table = "tbl_siswa"

class Tbl_akses(models.Model):
    id_akses = models.IntegerField(primary_key=True)
    nama_akses = models.CharField(max_length=20)

    class Meta:
        db_table = "tbl_akses"

class Tbl_guru(models.Model):
    id_guru = models.CharField(primary_key=True, max_length=9)
    nama_guru = models.CharField(max_length=50)
    email_guru = models.CharField(max_length=50)
    password_guru = models.CharField(max_length=100)
    id_akses = models.ForeignKey(Tbl_akses, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "tbl_guru"

class Tbl_kategori(models.Model):
    id_kategori = models.CharField(primary_key=True, max_length=3)
    nama_kategori = models.CharField(max_length=20)

    class Meta:
        db_table = "tbl_kategori"

class Tbl_nama_acara(models.Model):
    id_nama_acara = models.CharField(max_length=6, primary_key=True)
    id_kategori = models.ForeignKey(Tbl_kategori, on_delete=models.CASCADE)
    nama_acara = models.CharField(max_length=20)

    class Meta:
        db_table = "tbl_nama_acara"

class Tbl_acara(models.Model):
    id_acara = models.AutoField(primary_key=True) 
    id_nama_acara = models.ForeignKey(Tbl_nama_acara, on_delete=models.CASCADE, null=True)
    waktu_acara = models.DateTimeField() # not current time

    class Meta:
        db_table = "tbl_acara"

class Tbl_jampel(models.Model):
    id_jampel = models.AutoField(primary_key=True)
    nama_jampel = models.CharField(max_length=5)
    waktu_jampel = models.TimeField()

    class Meta:
        db_table = "tbl_jampel"

class Tbl_absen_ami(models.Model):
    id_absen_ami = models.AutoField(primary_key=True)
    id_jampel = models.ForeignKey(Tbl_jampel, on_delete=models.CASCADE, default=None)
    id_acara = models.ForeignKey(Tbl_acara, on_delete=models.CASCADE)
    id_siswa = models.ForeignKey(Tbl_siswa, on_delete=models.CASCADE)
    kehadiran = models.BooleanField()
    kerapihan = models.BooleanField()
    kebersihan = models.BooleanField()

    class Meta:
        db_table = "tbl_absen_ami"

class Tbl_absen(models.Model):
    id_absen = models.AutoField(primary_key=True)
    id_acara = models.ForeignKey(Tbl_acara, on_delete=models.CASCADE)
    id_siswa = models.ForeignKey(Tbl_siswa, on_delete=models.CASCADE)
    waktu_absensi = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id_absen:
            self.waktu_absensi = timezone.now()
        return super(Tbl_absen, self).save(*args, **kwargs)

    class Meta:
        db_table = "tbl_absen"

class Tbl_validasi(models.Model):
    id_validasi = models.AutoField(primary_key=True)
    id_absen = models.OneToOneField(Tbl_absen, on_delete=models.CASCADE, related_name="validasi_absen")
    id_guru = models.ForeignKey(Tbl_guru, on_delete=models.CASCADE)
    waktu_validasi = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id_validasi:
            self.waktu_validasi = timezone.now()
        return super(Tbl_validasi, self).save(*args, **kwargs)

    class Meta:
        db_table = "tbl_validasi"