import random
import re
from sqlite3 import Cursor
import uuid
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from utils.query import *


# Create your views here.
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get("password")

        # Assuming cursor is defined and connected to your database
        cursor.execute(
            f'SELECT * FROM akun WHERE email = %s AND password = %s', [email, password])
        user = cursor.fetchone()

        if user == None:
            cursor.execute(
                f'SELECT * FROM label WHERE email = %s AND password = %s', [email, password])
            label = cursor.fetchone()
            if label != None:
                id_label = label[0]
                cursor.execute(
                    f'SELECT * FROM label WHERE id = %s', [id_label])
                label_album = cursor.fetchall()
                context = {
                    'role': 'label',
                    'label_album': label_album,
                    'id': id_label,
                    'name': label[1],
                    'email': label[2],
                    'password': label[3],
                    'phone_number': label[4],
                    'id_pemilik_hak_cipta': label[5]
                }
                response = render(request, 'dashboard_label.html', context)
                response.set_cookie('role', 'label')
                response.set_cookie('email', email)
                response.set_cookie('id', id_label)
                response.set_cookie('id_pemilik_hak_cipta', label[5])
                return response
            else:
                context = {
                    'message': 'Mohon cek kembali email dan password anda.',
                    'status': 'error',
                    'role': None,
                }
                return render(request, 'login.html', context)
        else:
            id_user_artist = ''
            id_user_songwriter = ''
            id_pemilik_hak_cipta_artist = ""
            id_pemilik_hak_cipta_songwriter = ""
            status_langganan = "NonPremium"
            isArtist = False
            isSongwriter = False
            isLabel = False
            isPodcaster = False
            # artist
            cursor.execute(
                f'SELECT * FROM artist WHERE email_akun = %s', [email])
            artist = cursor.fetchone()
            if artist != None:
                id_user_artist = artist[0]
                id_pemilik_hak_cipta_artist = artist[2]
                isArtist = True
                cursor.execute(
                    f'SElect * from song where id_artist = %s', [id_user_artist])
                list_songs_artist = cursor.fetchall()

            # songwriter
            cursor.execute(
                f'SELECT * FROM songwriter WHERE email_akun = %s', [email])
            songwriter = cursor.fetchone()
            if songwriter != None:
                id_user_songwriter = songwriter[0]
                id_pemilik_hak_cipta_songwriter = songwriter[2]
                isSongwriter = True
                cursor.execute(
                    f'SELECT id_song from  songwriter_write_song where id_songwriter= %s', [id_user_songwriter])
                list_songs_songwriter = cursor.fetchall()

            # podcaster
            cursor.execute(
                f'select * from podcaster where email = %s', [email])
            podcaster = cursor.fetchone()
            print(podcaster)
            if podcaster != None:
                isPodcaster = True
                cursor.execute(
                    f'Select * from podcast where email_podcaster = %s', [email])
                list_episode = cursor.fetchall()

            cursor.execute(
                f'select * from user_playlist where email_pembuat = \'{email}\'')
            records_user_playlist = cursor.fetchall()

            cursor.execute(
                f'SELECT * FROM premium WHERE email = %s', [email])
            premium = cursor.fetchone()
            if premium != None:
                status_langganan = "Premium"

            verified_role = []
            if isArtist:
                verified_role.append('Artist')
            if isSongwriter:
                verified_role.append('Songwriter')
            if isPodcaster:
                verified_role.append('Podcaster')
            if verified_role == []:
                role_verif = 'User'
            else:
                role_verif = ', '.join(verified_role)

            context = {
                'role': role_verif,
                'status_langganan': status_langganan,
                'isArtist': isArtist,
                'isSongwriter': isSongwriter,
                'isPodcaster': isPodcaster,
                'email': user[0],
                'name': user[2],
                'gender': user[3],
                'tempat_lahir': user[4],
                'tanggal_lahir': user[5],
                'kota_asal': user[7],

            }
            print(role_verif)

            response = render(request, 'dashboard.html', context)
            response.set_cookie('role', role_verif)
            response.set_cookie('email', email)
            response.set_cookie('id_user_artist', id_user_artist)
            response.set_cookie('id_user_songwriter', id_user_songwriter)
            response.set_cookie('idPemilikCiptaArtist',
                                id_pemilik_hak_cipta_artist)
            response.set_cookie('idPemilikCiptaSongwriter',
                                id_pemilik_hak_cipta_songwriter)
            response.set_cookie('status_langganan', status_langganan)
            response.set_cookie('isArtist', isArtist)
            response.set_cookie('isSongwriter', isSongwriter)
            response.set_cookie('isPodcaster', isPodcaster)

            return response

        # Uncomment and adjust the following based on your logic
        # if user:
        #     return render(request, "home.html")
        # else:
        #     return render(request, "login.html")

    return render(request, "login.html")


def home(request):
    return render(request, "home.html")


def register(request):
    return render(request, "register.html")


def register_user(request):
    if request.method == "POST":
        connection, cursor = get_database_cursor()
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        gender = request.POST.get('gender')
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        kota_asal = request.POST.get('kota_asal')
        podcaster = request.POST.get('podcaster')
        artist = request.POST.get('artist')
        songwriter = request.POST.get('songwriter')

        # check email is already registered or not
        cursor.execute(f'select * from akun where email = \'{email}\'')
        records = cursor.fetchmany()
        if len(records) > 0:
            context = {
                'message': 'Email sudah terdaftar',
            }
            return render(request, 'register_user.html', context)

        # insert data to database
        try:
            is_verified = bool(podcaster or artist or songwriter)
            cursor.execute(
                f'insert into akun values (\'{email}\',\'{password}\',\'{nama}\',{gender},\'{tempat_lahir}\',\'{tanggal_lahir}\',\'{is_verified}\',\'{kota_asal}\')'
            )
            cursor.execute(
                f'insert into nonpremium values (\'{email}\')'
            )

            connection.commit()

            return redirect('authentication:login')

        except Exception as err:
            connection.rollback()
            print("Oops! An exception has occured:", err)
            print("Exception TYPE:", type(err))
            # err slice to get only error message
            err = str(err).split('CONTEXT')[0]
            context = {
                'message': err,
            }

            return render(request, 'register_user.html', context)

    return render(request, "register_user.html")


def register_label(request):
    connection, cursor = get_database_cursor()
    email = request.POST.get('email')
    password = request.POST.get('password')
    nama = request.POST.get('nama')
    kontak = request.POST.get('kontak')

    # # check email is valid or not
    # regex = re.compile(
    #     r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    # if not re.fullmatch(regex, email):
    #     context = {
    #         'message': 'Email tidak valid',
    #     }
    #     return render(request, 'register_label.html', context)

    # if data is not complete
    if not email or not password or not nama or not kontak:
        context = {
            'message': 'Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu',
        }
        return render(request, 'register_label.html', context)

    # check email is already registered or not
    cursor.execute(f'select * from akun where email = \'{email}\'')
    records = cursor.fetchmany()
    if len(records) > 0:
        context = {
            'message': 'Email sudah terdaftar',
        }
        return render(request, 'register_label.html', context)

    cursor.execute(f'select * from label where email = \'{email}\'')
    records = cursor.fetchmany()
    if len(records) > 0:
        context = {
            'message': 'Email sudah terdaftar',
        }
        return render(request, 'register_label.html', context)

    # insert data to database
    try:
        id_label = str(uuid.uuid4())
        id_pemilik_hak_cipta = str(uuid.uuid4())
        list_rate_royalti = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        rate_royalti = random.choice(list_rate_royalti)
        cursor.execute(
            f'insert into pemilik_hak_cipta values (\'{id_pemilik_hak_cipta}\', \'{rate_royalti}\')')
        cursor.execute(
            f'insert into label values (\'{id_label}\', \'{nama}\', \'{email}\', \'{password}\', \'{kontak}\', \'{id_pemilik_hak_cipta}\')')

        connection.commit()

        return redirect('authentication:login')

    except Exception as err:
        connection.rollback()
        print("Oops! An exception has occured:", err)
        print("Exception TYPE:", type(err))
        # err slice to get only error message
        err = str(err).split('CONTEXT')[0]
        context = {
            'message': err,
        }

        return render(request, 'register_label.html', context)


def logout(request):
    response = HttpResponseRedirect(reverse('authentication:login'))
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response
