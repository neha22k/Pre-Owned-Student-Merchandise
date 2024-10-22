from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('UserLoginAction', views.UserLoginAction, name="UserLoginAction"),	   
	       path('Register', views.Register, name="Register"),
	       path('RegisterAction', views.RegisterAction, name="RegisterAction"),
	       path('SaleProduct', views.SaleProduct, name="SaleProduct"),
	       path('SaleProductAction', views.SaleProductAction, name="SaleProductAction"),
	       path('SearchProducts', views.SearchProducts, name="SearchProducts"),
	       path('SearchProductsAction', views.SearchProductsAction, name="SearchProductsAction"),
	       path('Feedback', views.Feedback, name="Feedback"),
	       path('FeedbackAction', views.FeedbackAction, name="FeedbackAction"),
	       path('AdminLogin', views.AdminLogin, name="AdminLogin"),
	       path('AdminLoginAction', views.AdminLoginAction, name="AdminLoginAction"),	
	       path('ViewUsers', views.ViewUsers, name="ViewUsers"),
	       path('ViewProducts', views.ViewProducts, name="ViewProducts"),
	       path('ViewFeedback', views.ViewFeedback, name="ViewFeedback"),
	       path('ViewHistory', views.ViewHistory, name="ViewHistory"),
	       path('PurchaseProduct', views.PurchaseProduct, name="PurchaseProduct"),
           path('payment/', views.PaymentView.as_view(), name='Payment'),
           path('upi_payment/', views.UPIPaymentView.as_view(), name='UPIPayment'),  # Ensure this line exists
]