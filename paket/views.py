import uuid
from django.shortcuts import redirect, render
from utils.query import get_database_cursor
from datetime import datetime, timedelta

# Create your views here.
def paket(request):
    connection, cursor = get_database_cursor()
    cursor.execute("\
        select * from paket"
    )
    paket = cursor.fetchall()
    context = {
        "paket": paket
    }
    print(paket)
    return render(request, "paket.html", context)

def paket_payment(request, nama_paket):
    connection, cursor = get_database_cursor()

    print(nama_paket)
    cursor.execute(f"\
        select * from paket where jenis='{nama_paket}'"
    )
    paket = cursor.fetchone()
    context = {
        "paket": paket
    }
    print(paket)

    if request.method == "POST":
        metode = request.POST.get("metode")
        email = request.COOKIES.get("email")
        transaction_id = str(uuid.uuid4())
        nominal = paket[1]
        # Mendapatkan tanggal dan waktu sekarang
        sekarang = datetime.now()

        hari = 0
        if nama_paket == "1 bulan":
            hari = 30
        elif nama_paket == "3 bulan":
            hari = 90
        elif nama_paket == "6 bulan":
            hari = 180
        else:
            hari = 365
        
        # Menambahkan masa paket
        akhir_paket = sekarang + timedelta(days=hari)

        sekarang = sekarang.strftime("%Y-%m-%d %H:%M:%S") 
        akhir_paket = akhir_paket.strftime("%Y-%m-%d %H:%M:%S") 

        print(email, metode,nama_paket, nominal, sekarang, akhir_paket, transaction_id)
        cursor.execute(f"\
            INSERT INTO TRANSACTION VALUES ('{transaction_id}', '{nama_paket}', '{email}',\
                '{sekarang}', '{akhir_paket}', '{metode}', {nominal})")
        cursor.execute(f"\
            INSERT INTO PREMIUM VALUES ('{email}')")
        connection.commit()
        return redirect('dashboard:riwayat')


    return render(request, "paket_payment.html", context)

def riwayat(request):
    connection, cursor = get_database_cursor()
    email = request.COOKIES.get("email")
    cursor.execute(f"\
        select * from transaction where email='{email}'"
    )
    riwayat = cursor.fetchall()
    context = {
        "riwayat": riwayat
    }
    print(riwayat)
    return render(request, "riwayat.html", context)