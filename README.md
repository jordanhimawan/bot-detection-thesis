# bot-detection-thesis

Sistem terdistribusi ini terdiri dari tiga (3) buah _classifier_ dengan menggunakan algoritma XGBoost (_Xtreme Gradient Boosting_). Sistem ini menggunakan RabbitMQ sebagai _message broker_ sehingga data Twitter dapat dikirim secara terbagi rata dari _crawler_ sebagai _producer_ menuju ke ketiga _classifier_ sebagai _consumer_. Data Twitter diambil _crawler_ menggunakan pustaka Twint.

Sistem ini dapat dijalankan dengan sistem operasi Linux.
