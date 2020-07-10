from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

# Create your views here.
def to_login_views(request):
    try:
        del request.session['namacook']
        del request.session['idcook']
        del request.session['kelascook']
        del request.session['idkelas']
        del request.session['idnamaacaracook']
        del request.session['idacara']
    except:
        pass
    return render(request, 'login/Loginsiswa.html', {})

def to_login_guru_views(request):
    try:
        del request.session['namacook']
        del request.session['idcook']
        del request.session['kelascook']
        del request.session['idkelas']
        del request.session['idnamaacaracook']
        del request.session['idacara']
    except:
        pass
    return render(request, 'login/Loginguru.html', {})

def login_views(request):
    if request.method == "POST":
        tbl_kategori = Tbl_kategori.objects.all()
        if request.POST['nis'] != "":
            try:
                tbl_siswa = Tbl_siswa.objects.get(id_siswa=request.POST['nis'])
            except Tbl_siswa.DoesNotExist:
                tbl_siswa = None
            if tbl_siswa is not None:
                if tbl_siswa.password_siswa == request.POST['password']:
                    context = {
                        "tbl_siswa": tbl_siswa,
                        "tbl_kategori": tbl_kategori,
                        "absen_amis": Tbl_absen_ami.objects.filter(Q(id_acara__waktu_acara__range=(timezone.now() - timedelta(days=7), timezone.now())), Q(id_siswa_id__exact=request.POST['nis'])),
                        "validasis": Tbl_validasi.objects.filter(Q(id_absen__id_acara__waktu_acara__range=(timezone.now() - timedelta(days=7), timezone.now())), Q(id_absen__id_siswa_id__exact=request.POST['nis'])),
                    }
                    request.session['idcook'] = tbl_siswa.id_siswa
                    request.session['namacook'] = tbl_siswa.nama_siswa
                    request.session['kelascook'] = tbl_siswa.id_kelas.nama_kelas
                    return render(request, 'siswa/Kategori_Siswa.html', context)
                else:
                    messages.warning(request, 'Password tidak sesuai dengan di database kami! Cobalah lagi!', extra_tags='alert')
                    return redirect(to_login_views)
            else:
                messages.warning(request, 'NIS yang dimasukan tidak sesuai dengan di database kami! Cobalah lagi!', extra_tags='alert')
                return redirect(to_login_views)
        else:
            messages.warning(request, 'NIS masih belum terisi!', extra_tags='alert')
            return redirect(to_login_views)
    else:
        return redirect(to_login_views) # buat logout atau jika bukan post

def login_guru_views(request):
    if request.method == "POST":
        tbl_kategori = Tbl_kategori.objects.all()
        if request.POST['nik'] != "":
            try:
                tbl_guru = Tbl_guru.objects.get(id_guru=request.POST['nik'])
            except Tbl_guru.DoesNotExist:
                tbl_guru = None
            if tbl_guru is not None:
                if tbl_guru.password_guru == request.POST['password']:
                    tbl_kelas = Tbl_kelas.objects.all()
                    if tbl_guru.id_akses_id == 1: # admin = goes to dashboard admin
                        request.session['idcook'] = tbl_guru.id_guru
                        request.session['namacook'] = tbl_guru.nama_guru
                        return redirect(to_dashboard_admin_views)
                    elif tbl_guru.id_akses_id == 2: # walas = kayak siswa tapi ada pilihkelas, disiplin di kategori, dan validasi
                        context = {
                            "tbl_guru": tbl_guru,
                            "tbl_kategori": tbl_kategori,
                        }
                        request.session['idcook'] = tbl_guru.id_guru
                        request.session['namacook'] = tbl_guru.nama_guru
                        return render(request, "guru/walas/Kategori_Walas.html", context)
                    elif tbl_guru.id_akses_id == 3: # nonwalas-guru = cuman ke penilaian ami
                        context = {
                            "tbl_guru": tbl_guru,
                            "tbl_kelas": tbl_kelas,
                        }
                        return render(request, "guru/nonwalas_guru/KelasAMI.html", context)
                    elif tbl_guru.id_akses_id == 4: # nonwalas-manajemen = cuman ke report
                        request.session['idcook'] = tbl_guru.id_guru
                        request.session['namacook'] = tbl_guru.nama_guru
                        context = {
                            "nama_guru": tbl_guru.nama_guru,
                            "tbl_kelas": tbl_kelas,
                            "tbl_siswa": Tbl_siswa.objects.all(),
                            "tbl_nama_acara": Tbl_nama_acara.objects.all(),
                            "tbl_validasi": Tbl_validasi.objects.all(),
                            "tbl_absen_ami": Tbl_absen_ami.objects.all(),
                        }
                        return render(request, "guru/nonwalas_manajemen/Laporan.html", context)
                    else:
                        return HttpResponse("<center> KAU SEHARUSNYA TIDAK MENAMBAHKAN ID KE-"+ tbl_guru.id_akses_id +"!!!  :| </center>")
                else:
                    messages.warning(request, 'Password tidak sesuai dengan di database kami! Cobalah lagi!', extra_tags='alert')
                    return redirect(to_login_guru_views)
            else:
                messages.warning(request, 'NIK yang dimasukan tidak sesuai dengan di database kami! Cobalah lagi!', extra_tags='alert')
                return redirect(to_login_guru_views)
        else:
            messages.warning(request, 'NIK masih belum terisi!', extra_tags='alert')
            return redirect(to_login_guru_views)
    else:
        return redirect(to_login_guru_views) # buat logout atau jika bukan post     

def absensave_views(request):
    if request.method == "POST":
        if request.session.has_key('idcook'):
            idsiswa = request.session['idcook']
        else:
            idsiswa = "tidak ada id"
        tbl_acara = Tbl_acara.objects.get(id_acara=request.POST['submitidacara'])
        tbl_absen_save = Tbl_absen(
            id_acara_id = tbl_acara.id_acara,
            id_siswa_id = idsiswa,
        )
        tbl_absen_save.save()
        return redirect(to_acara_views)
    else:
        return redirect(login_views)

def to_acara_views(request):
    if request.method == "POST":
        if request.session.has_key('namacook') and request.session.has_key('kelascook'):
            nama = request.session['namacook']
            kelas = request.session['kelascook']
        else:
            nama = "tidak ada nama"
            kelas = "tidak ada kelas"
        context = {
            "acaras": Tbl_acara.objects.filter(id_nama_acara__id_kategori__exact=request.POST['idkategori']),
            # "namaacaras": Tbl_nama_acara.objects.filter(id_kategori__exact=request.POST['idkategori']),
            "kategori": Tbl_kategori.objects.get(id_kategori=request.POST['idkategori']),
            "nama": nama,
            "kelas": kelas,
        }
        return render(request, 'siswa/Acara_Siswa.html', context)
    else:
        return redirect(login_views)

def to_acara_walas_views(request):
    if request.method == "POST":
        if request.session.has_key('namacook'):
            nama = request.session['namacook']
        else:
            nama = "tidak ada nama"
        context = {
            "acaras": Tbl_acara.objects.filter(id_nama_acara__id_kategori__exact=request.POST['idkategori']),
            # "namaacaras": Tbl_nama_acara.objects.filter(id_kategori__exact=request.POST['idkategori']),
            "kategori": Tbl_kategori.objects.get(id_kategori=request.POST['idkategori']),
            "nama": nama,
            "todaydate": timezone.now().date(),
        }
        return render(request, 'guru/walas/Acara_Walas.html', context)
    else:
        return redirect(login_guru_views)

def to_pilihkelas_walas_views(request):
    if request.method == "POST":
        request.session['idacara'] = request.POST['idacara']
        request.session['idnamaacaracook'] = request.POST['idnamaacara']
        if request.session.has_key('namacook'):
            nama = request.session['namacook']
        else:
            nama = "tidak ada nama"
        context = {
            "nama": nama,
            "tbl_kelas": Tbl_kelas.objects.all(),
        }
        return render(request, "guru/walas/Kelas_Walas.html", context)
    else:
        return redirect(to_login_guru_views)

def to_validasi_walas_views(request):
    if request.method == "POST":
        tbl_kelas = Tbl_kelas.objects.get(id_kelas=request.POST['idkelas'])
        if request.session['idnamaacaracook'] == "AMI":
            context = {
                "namakelas": tbl_kelas.nama_kelas,
                "tbl_jampels": Tbl_jampel.objects.all(),
                "siswas": Tbl_siswa.objects.filter(id_kelas__exact=request.POST['idkelas']),
            }
            return render(request, "guru/walas/AMI.html", context)
        else:         
            tbl_nama_acara = Tbl_nama_acara.objects.get(id_nama_acara=request.session['idnamaacaracook'])
            tbl_absen = Tbl_absen.objects.filter(Q(id_siswa__id_kelas__exact=request.POST['idkelas']), Q(id_acara__id_nama_acara__exact=request.session['idnamaacaracook']))
            context = {
                "namaacara": tbl_nama_acara.nama_acara,
                "namakelas": tbl_kelas.nama_kelas,
                "tbl_absen": tbl_absen,
                "todaydate": timezone.now().date(),
            }
            return render(request, "guru/walas/Validasi_Walas.html", context)
    else:
        return redirect(login_guru_views)

def validasi_views(request):
    if request.method == "POST":
        for i in range(int(request.POST['lengthloop'])):
            amount = i + 1
            if request.session.has_key('idcook'):
                idg = request.session['idcook']
                if 'Check'+str(amount) in request.POST:
                    tbl_validasi_save = Tbl_validasi(
                        id_absen_id = request.POST['Check' + str(amount)],
                        id_guru_id = idg,
                    )
                    tbl_validasi_save.save()
            else:
                return redirect(to_login_guru_views)
        return redirect(to_login_guru_views)
    else:
        return redirect(to_login_guru_views)

def to_ami_views(request):
    if request.method == "POST":
        tbl_kelas = Tbl_kelas.objects.get(id_kelas=request.POST['idkelas'])
        context = {
            "namakelas": tbl_kelas.nama_kelas,
            "tbl_jampels": Tbl_jampel.objects.all(),
            "siswas": Tbl_siswa.objects.filter(id_kelas__exact=request.POST['idkelas']),
        }
        return render(request, "guru/nonwalas_guru/AMI.html", context)
    else:
        return redirect(login_guru_views)

def ami_validasi_views(request):
    if request.method == "POST":
        try:
            request.session['idacara']
        except:
            return redirect(to_login_guru_views)
        for h in range(int(request.POST['idstart']), int(request.POST['idend']) + 1):
            amount = 0
            for i in range(int(request.POST['lengthloop'])):
                amount = i + 1 
                hadirvar = False
                rapihvar = False
                bersihvar = False
                if 'hadir'+str(amount) in request.POST:
                    hadirvar = True
                if 'rapih'+str(amount) in request.POST:
                    rapihvar = True
                if 'bersih'+str(amount) in request.POST:
                    bersihvar = True
                if 'validasi'+str(amount) in request.POST:
                    acara = Tbl_acara.objects.get(id_nama_acara_id="AMI")
                    tbl_absenami_save = Tbl_absen_ami(
                        id_jampel_id = h,
                        id_acara_id = acara.id_acara,
                        id_siswa_id = request.POST['validasi' + str(amount)],
                        kehadiran = hadirvar,
                        kerapihan = rapihvar,
                        kebersihan = bersihvar,
                    )
                    tbl_absenami_save.save()
                else:
                    return redirect(to_login_guru_views)
        return redirect(to_login_guru_views)
    else:
        return redirect(to_login_guru_views)

def to_dashboard_admin_views(request):
    if request.session.has_key('namacook'):
        nama = request.session['namacook']
    else:
        nama = "tidak ada nama"
    context = {
        "jumlah_siswa": len(Tbl_siswa.objects.all()),
        "jumlah_guru": len(Tbl_guru.objects.all()), 
        "jumlah_acara": len(Tbl_acara.objects.all()),
        "jumlah_kelas": len(Tbl_kelas.objects.all()),
        "nama_guru": nama,
    }
    return render(request, "guru/admin/Dashboard.html", context)

def to_guru_admin_views(request):
    if request.session.has_key('namacook'):
        nama = request.session['namacook']
    else:
        nama = "tidak ada nama"
    context = {
        "tbl_guru": Tbl_guru.objects.all(),
        "nama_guru": nama,
    }
    return render(request, "guru/admin/Guru.html", context)

def to_tambahguru_admin_views(request):
    if request.session.has_key('namacook'):
        nama = request.session['namacook']
    else:
        nama = "tidak ada nama"
    context = {
        "nama_guru": nama,
        "tbl_akses": Tbl_akses.objects.all(),
    }
    return render(request, "guru/admin/tambah_guru.html", context)

def tambahguru_admin_views(request):
    if request.method == "POST":
        tbl_guru_save = Tbl_guru(
            id_guru = request.POST['NIK'],
            nama_guru = request.POST['nama'],
            email_guru = request.POST['email'],
            password_guru = request.POST['password'],
            id_akses_id = request.POST['hakakses'],
        )
        tbl_guru_save.save()
        return redirect(to_guru_admin_views)
    else:
        return redirect(login_guru_views)

def to_editguru_admin_views(request):
    if request.method == "POST":
        if request.session.has_key('namacook'):
            nama = request.session['namacook']
        else:
            nama = "tidak ada nama"
        context = {
            "tbl_guru": Tbl_guru.objects.get(id_guru=request.POST['idguru']),
            "tbl_akses": Tbl_akses.objects.all(),
            "nama_guru": nama,
        }
        return render(request, "guru/admin/edit_guru.html", context)
    else:
        return redirect(login_guru_views)

def editguru_admin_views(request):
    if request.method == "POST":
        tbl_guru = Tbl_guru.objects.get(id_guru=request.POST['NIK'])
        tbl_guru.id_guru = request.POST['NIK']
        tbl_guru.nama_guru = request.POST['nama']
        tbl_guru.email_guru = request.POST['email']
        tbl_guru.password_guru = request.POST['password']
        tbl_guru.id_akses_id = request.POST['hakakses']
        tbl_guru.save()
        return redirect(to_guru_admin_views)
    else:
        return redirect(login_guru_views)

def hapusguru_admin_views(request):
    if request.method == "POST":
        tbl_guru = Tbl_guru.objects.get(id_guru=request.POST['idguru'])
        tbl_guru.delete()
        return redirect(to_guru_admin_views)
    else:
        return redirect(login_guru_views)

def to_siswa_admin_views(request):
    if request.session.has_key('namacook'):
        nama = request.session['namacook']
    else:
        nama = "tidak ada nama"
    context = {
        "tbl_siswa": Tbl_siswa.objects.all(),
        "nama_guru": nama,
    }
    return render(request, "guru/admin/Siswa.html", context)

def to_tambahsiswa_admin_views(request):
    if request.session.has_key('namacook'):
        nama = request.session['namacook']
    else:
        nama = "tidak ada nama"
    context = {
        "nama_guru": nama,
        "tbl_kelas": Tbl_kelas.objects.all(),
    }
    return render(request, "guru/admin/tambah_siswa.html", context)

def tambahsiswa_admin_views(request):
    if request.method == "POST":
        tbl_siswa_save = Tbl_siswa(
            id_siswa = request.POST['NIS'],
            nama_siswa = request.POST['nama'],
            email_siswa = request.POST['email'],
            id_kelas_id = request.POST['kelas'],
            password_siswa = request.POST['password'],
        )
        tbl_siswa_save.save()
        return redirect(to_siswa_admin_views)
    else:
        return redirect(login_guru_views)

def to_editsiswa_admin_views(request):
    if request.method == "POST":
        if request.session.has_key('namacook'):
            nama = request.session['namacook']
        else:
            nama = "tidak ada nama"
        context = {
            "tbl_siswa": Tbl_siswa.objects.get(id_siswa=request.POST['idsiswa']),
            "tbl_kelas": Tbl_kelas.objects.all(),
            "nama_guru": nama,
        }
        return render(request, "guru/admin/edit_siswa.html", context)
    else:
        return redirect(login_guru_views)

def editsiswa_admin_views(request):
    if request.method == "POST":
        tbl_siswa = Tbl_siswa.objects.get(id_siswa=request.POST['NIS'])
        tbl_siswa.id_siswa = request.POST['NIS']
        tbl_siswa.nama_siswa = request.POST['nama']
        tbl_siswa.email_siswa = request.POST['email']
        tbl_siswa.id_kelas_id = request.POST['kelas']
        tbl_siswa.password_siswa = request.POST['password']
        tbl_siswa.save()
        return redirect(to_siswa_admin_views)
    else:
        return redirect(login_guru_views)

def hapussiswa_admin_views(request):
    if request.method == "POST":
        tbl_siswa = Tbl_siswa.objects.get(id_siswa=request.POST['idsiswa'])
        tbl_siswa.delete()
        return redirect(to_siswa_admin_views)
    else:
        return redirect(login_guru_views)

def to_kelas_admin_views(request):
    if request.session.has_key('namacook'):
        nama = request.session['namacook']
    else:
        nama = "tidak ada nama"
    context = {
        "tbl_kelas": Tbl_kelas.objects.all(),
        "tbl_siswa": Tbl_siswa.objects.all(),
        "nama_guru": nama,
    }
    return render(request, "guru/admin/Kelas.html", context)

def to_tambahkelas_admin_views(request):
    if request.session.has_key('namacook'):
        nama = request.session['namacook']
    else:
        nama = "tidak ada nama"
    context = {
        "nama_guru": nama,
    }
    return render(request, "guru/admin/tambah_kelas.html", context)

def tambahkelas_admin_views(request):
    if request.method == "POST":
        tbl_kelas_save = Tbl_kelas(
            id_kelas = request.POST['id'],
            nama_kelas = request.POST['nama'],
        )
        tbl_kelas_save.save()
        return redirect(to_kelas_admin_views)
    else:
        return redirect(login_guru_views)

def to_editkelas_admin_views(request):
    if request.method == "POST":
        if request.session.has_key('namacook'):
            nama = request.session['namacook']
        else:
            nama = "tidak ada nama"
        context = {
            "tbl_kelas": Tbl_kelas.objects.get(id_kelas=request.POST['idkelas']),
            "nama_guru": nama,
        }
        return render(request, "guru/admin/edit_kelas.html", context)
    else:
        return redirect(login_guru_views)

def editkelas_admin_views(request):
    if request.method == "POST":
        tbl_kelas = Tbl_kelas.objects.get(id_kelas=request.POST['idkelas'])
        tbl_kelas.id_kelas = request.POST['id']
        tbl_kelas.nama_kelas = request.POST['nama']
        tbl_kelas.save()
        return redirect(to_kelas_admin_views)
    else:
        return redirect(login_guru_views)

def hapuskelas_admin_views(request):
    if request.method == "POST":
        tbl_kelas = Tbl_kelas.objects.get(id_kelas=request.POST['idkelas'])
        tbl_kelas.delete()
        return redirect(to_kelas_admin_views)
    else:
        return redirect(login_guru_views)

def to_acara_admin_views(request):
    if request.session.has_key('namacook'):
        nama = request.session['namacook']
    else:
        nama = "tidak ada nama"
    context = {
        "tbl_acara": Tbl_acara.objects.all(),
        "nama_guru": nama,
    }
    return render(request, "guru/admin/Acara.html", context)

def to_tambahacara_admin_views(request):
    if request.session.has_key('namacook'):
        nama = request.session['namacook']
    else:
        nama = "tidak ada nama"
    context = {
        "nama_guru": nama,
        "tbl_nama_acara": Tbl_nama_acara.objects.all(),
    }
    return render(request, "guru/admin/tambah_acara.html", context)

def tambahacara_admin_views(request):
    if request.method == "POST":
        tbl_acara_save = Tbl_acara(
            id_nama_acara_id = request.POST['nama'],
            waktu_acara = request.POST['waktu'],
        )
        tbl_acara_save.save()
        return redirect(to_acara_admin_views)
    else:
        return redirect(login_guru_views)

def to_editacara_admin_views(request):
    if request.method == "POST":
        if request.session.has_key('namacook'):
            nama = request.session['namacook']
        else:
            nama = "tidak ada nama"
        context = {
            "tbl_acara": Tbl_acara.objects.get(id_acara=request.POST['idacara']),
            "tbl_nama_acara": Tbl_nama_acara.objects.all(),
            "nama_guru": nama,
        }
        return render(request, "guru/admin/edit_acara.html", context)
    else:
        return redirect(login_guru_views)

def editacara_admin_views(request):
    if request.method == "POST":
        tbl_acara = Tbl_acara.objects.get(id_acara=request.POST['idacara'])
        tbl_acara.id_nama_acara_id = request.POST['nama']
        tbl_acara.waktu_acara = request.POST['waktu']
        tbl_acara.save()
        return redirect(to_acara_admin_views)
    else:
        return redirect(login_guru_views)

def hapusacara_admin_views(request):
    if request.method == "POST":
        tbl_acara = Tbl_acara.objects.get(id_acara=request.POST['idacara'])
        tbl_acara.delete()
        return redirect(to_acara_admin_views)
    else:
        return redirect(login_guru_views)

def laporankelas_admin_views(request):
    if request.method == "POST":
        try:
            request.session['namacook']
        except:
            return redirect(login_guru_views)
        request.session['idkelas'] = request.POST['idkelas']
        context = {
            "nama_guru": request.session['namacook'],
            "tbl_kelas": Tbl_kelas.objects.all(),
            "tbl_siswa": Tbl_siswa.objects.filter(id_kelas_id__exact=request.POST['idkelas']),
            "tbl_nama_acara": Tbl_nama_acara.objects.all(),
            "tbl_validasi": Tbl_validasi.objects.all(),
            "tbl_absen_ami": Tbl_absen_ami.objects.all(),
        }
        return render(request, "guru/nonwalas_manajemen/Laporan.html", context)
    else:
        return redirect(login_guru_views)

def laporantanggal_admin_views(request):
    if request.method == "POST":
        try:
            request.session['idkelas']
            request.session['namacook']
        except:
            return redirect(login_guru_views)
        context = {
            "nama_guru": request.session['namacook'],
            "tbl_siswa": Tbl_siswa.objects.filter(id_kelas_id__exact=request.session['idkelas']),
            "tbl_kelas": Tbl_kelas.objects.all(),
            "tbl_validasi": Tbl_validasi.objects.filter(Q(id_absen__id_acara__waktu_acara__range=(request.POST['start'], request.POST['end'])), Q(id_absen__id_siswa__id_kelas_id__exact=request.session['idkelas'])),
            "tbl_absen_ami": Tbl_absen_ami.objects.filter(Q(id_acara__waktu_acara__range=(request.POST['start'], request.POST['end'])), Q(id_siswa__id_kelas_id__exact=request.session['idkelas'])),
            "tbl_nama_acara": Tbl_nama_acara.objects.all(),
        }
        return render(request, "guru/nonwalas_manajemen/Laporan.html", context)
    else:
        return redirect(login_guru_views)