from django.urls import path
from . import views


urlpatterns = [
    path("",views.admins_home,name='admin'),
    path('admin_users',views.admins_home,name='admin'),
    path('admins_log',views.admins_log,name = 'admins_log'),
    path('admins_login',views.admins_login,name = 'admins_login'),
    path('admins_home',views.admins_home,name = 'admins_home'),

    path('admins_logout',views.admins_logout,name='admins_logout'),
    path('product_details',views.product_details,name='product_details'),
    path('add_products',views.add_products,name='add_products'),
    path('new_products',views.new_products,name='new_products'),
    path('edit_products/<int:id>',views.edit_products,name='edit_products'),
    path('pro_update/<int:id>',views.pro_update,name='pro_update'),
    path('product_delete/<int:id>',views.product_delete,name='product_delete'),

    path('category',views.categorys,name='category'),
    path('add_category',views.add_category,name='add_category'),
    path('new_category',views.new_category,name='new_category'),
    path('edit_category/<int:id>',views.edit_category,name='edit_category'),
    path('category_update/<int:id>',views.category_update,name='category_update'),
    path('category_delete/<int:id>',views.category_delete,name='category_delete'),

    path('user_block/<int:id>',views.user_block,name='user_block'),
    path('user_unblock/<int:id>',views.user_unblock,name='user_unblock'),

    path('add_subcategory',views.add_subcategory,name='add_subcategory'),
    path('new_subcategory',views.new_subcategory,name='new_subcategory'),
    path('subcategory_delete/<int:id>',views.subcategory_delete,name='subcategory_delete'),
    path('edit_subcategory/<int:id>',views.edit_subcategory,name='edit_subcategory'),
    path('subcategory_update/<int:id>',views.subcategory_update,name='subcategory_update'),

    path('order_details',views.order_details,name = 'order_details'),
    path('order_delete/<int:id>',views.order_delete,name = 'order_delete'),
    path('DashBoard',views.DashBoard,name = 'DashBoard'),
    path('StatusUpdate/<int:id>',views.StatusUpdate,name = 'StatusUpdate'),

    path('SalesReport',views.SalesReport,name = 'sales report'),
    path('sales_date_wise',views.sales_date_wise,name = 'sales_date_wise'),
    path('sales_year_wise',views.sales_year_wise,name = 'sales_year_wise'),

    path('Offers',views.Offers,name='Offers'),
    path('AddProductOffer',views.AddProductOffer,name='AddProductOffer'),
    path('EditProductOffer/<int:id>',views.EditProductOffer,name = 'EditProductOffer'),
    path('RmoveProductOffer/<int:id>', views.RmoveProductOffer, name="RmoveProductOffer"),

    path('AddCategoryOffer', views.AddCategoryOffer, name="AddCategoryOffer"),
    path('EditCategoryOffer/<int:id>', views.EditCategoryOffer, name="EditCategoryOffer"),
    path('RmoveCategoryOffer/<int:id>', views.RmoveCategoryOffer, name="RmoveCategoryOffer"),

    path('Coupon',views.coupon,name = 'Coupon'),
    path('AddCoupon',views.AddCoupon,name = 'AddCoupon'),
    path('couponEdit/<int:id>',views.couponEdit,name = 'couponEdit'),
    path('couponBlock/<int:id>', views.couponBlock, name="couponBlock"),
    path('couponUnblock/<int:id>', views.couponUnblock, name="couponUnblock"),
    path('couponRemove/<int:id>', views.couponRemove, name="couponRemove"),
]
