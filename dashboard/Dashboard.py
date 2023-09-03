import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membuat Data
df = pd.read_csv('E:\Progamming Project\Portofolio\Project_E-Commerce_Public_Dataset_by_dicoding\customers_dataset.csv')
data = pd.read_csv('E:\Progamming Project\Portofolio\Project_E-Commerce_Public_Dataset_by_dicoding\order_payments_dataset.csv')
data = data.drop(data[data['payment_type'].isin(['not_defined'])].index)

def analisa1():
    # Melakukan agregasi pada Pertanyaan 1
    customerstate = df.groupby('customer_state').agg({'customer_city':['count']})

    # Merapihkan bentuk DataFrame
    customerstate.columns = customerstate.columns.droplevel(1)
    customerstate = customerstate.sort_values(by='customer_city' ,ascending=False)
    customerstate = customerstate.reset_index()
    customerstate = customerstate.rename(columns={'customer_city':'total_customer'})
    
    return customerstate

def analisa2():
    # Melakukan agregasi pada Pertanyaan 2
    payment = data.groupby('payment_type').agg({'payment_value':['min','max','sum']})

    # Merapihkan bentuk DataFrame
    payment.columns = payment.columns.droplevel(0)
    payment = payment.rename(columns={
        'min':'Sales Terendah',
        'max':'Sales Tertinggi',
        'sum':'Total Sales'
        })
    payment = payment.reset_index().sort_values(by='Total Sales' ,ascending=False)
    
    return payment

def visual1():
    '''
    Menghasilkan Analisa Visualisasi pertanyaan ke-1
    ''' 
    # Membuat Canvas untuk Visualisasi
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    fig.suptitle('Total Customers by State', fontsize=20)

    # Membuat Informasi pada Visualisasi
    ax.bar(analisa1()['customer_state'], analisa1()['total_customer'])
    ax.set_xlabel('State', fontsize=16)
    ax.set_ylabel('Total Customers', fontsize=16)

    # Melihat hasil Visualisasi
    plt.tight_layout()
    st.pyplot(fig)

def visual2():
    '''
    Menghasilkan Analisa Visualisasi pertanyaan ke-2
    '''  
    # Membuat Canvas untuk Visualisasi
    fig, ax = plt.subplots(1, 3, figsize=(15, 6))
    fig.suptitle('Customers Payment System', fontsize=24)

    # Membuat list judul yang akan digunakan untuk Iterasi
    title = analisa2().columns[1:]

    # Melakukan Iterasi untuk Visualisasi data sekaligus
    for a, b in zip(ax, title):
        sns.set_palette('pastel')
        sns.barplot(x='payment_type', y=b, data=analisa2(), ax=a)
        a.set_title(b, fontsize=16)
        a.set_xlabel('Payment Type', fontsize=16)
        a.set_ylabel('')

    # Melihat Hasil Visualisasi
    plt.tight_layout()
    st.pyplot(fig)

def juduldashboard():
    # Membuat Judul Dashboard
    st.title('Dashboard Visualisasi Data')
    
def metricdash():
    # Membuat 3 kolom metrics
    col1, col2 = st.columns(2)
    
    # Membuat Informasi Tambahan Pada Dashboard
    with col1:
        sum_customer_state = analisa1()['total_customer'].sum()
        st.metric('Total Customer', value= sum_customer_state)
    
    with col2:
        sum_payment = analisa2()['Total Sales'].sum()
        st.metric('Total Sales', value= sum_payment)
        

# Membuat Presentasi hasil Analisa pertanyaan ke - 1
def dashboard1():
    # Membuat Deskripsi Penjelasan
    st.caption('Berdasarkan hasil analisa data geografi Total Customers dapat di simpulkan bahwa Customers State SP memiliki jumlah Orderan / pengiriman produk paling banyak di banding Customers State lainnya.')
    
    # Memvisualisasikan Dashboard
    visual1()
    
# Membuat Presentasi hasil Analisa pertanyaan ke - 2
def dashboard2():
    # Membuat Deskripsi Penjelasan
    st.caption('Berdasarkan hasil analisa pola system Pembayaran dapat di simpulkan bahwa System Pembayaran Kartu Credit lebih sering di terapkan di banding System Pembayaran lainnya, hal ini di buktikan dengan Total Sales & Penjualan Tertinggi yang di dominasi oleh Kartu Credit')

    # Memvisualisasikan Dashboard
    visual2()

if __name__ == '__main__':
    juduldashboard()
    metricdash()
    dashboard1()
    dashboard2()