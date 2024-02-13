from azbankgateways import models as bank_models, default_settings as settings
from django.shortcuts import get_object_or_404, reverse, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import Http404

from .models import Course, UserCourse
from apps.payment.models import Order, OrderItem


# Render CoursesList view
class CoursesListView(LoginRequiredMixin, ListView):
    template_name = 'course/list.html'
    model = Course

    def filter(self, objects):
        q = self.request.GET.get('type')
        if q:
            objects = objects.filter(payment_type=q)
        return objects

    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True)
        return self.filter(queryset)


# Render CourseDetail view
class CourseDetailView(LoginRequiredMixin, DetailView):
    template_name = 'course/details.html'
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_course'] = UserCourse.objects.filter(course=self.object, user=self.request.user).exists()

        return context


# Render UserCourseList view
class UserCourseListView(LoginRequiredMixin, ListView):
    template_name = 'course/user_list.html'
    model = Course

    def get_queryset(self):
        queryset = Course.objects.filter(user_courses__user=self.request.user)
        return queryset


# PurchaseCourse view
class PurchaseCourseView(LoginRequiredMixin, View):
    """ Create order to purchase courses. """

    def has_course(self, obj):
        """ Check user purchased course before or not. """
        if UserCourse.objects.filter(user=self.request.user, course=obj).exists():
            raise Http404

    def post(self, request):
        pk = request.POST.get('pk')
        obj = get_object_or_404(Course, pk=pk)

        # Check user has course or not
        self.has_course(obj)

        # Create order
        order = Order.objects.create(
            user=request.user,
            payable_price=obj.selling_price,
            discount_price=int(obj.price - obj.selling_price),
            callback_url=reverse('course:add_course'),
        )

        OrderItem.objects.create(order=order, item_object=obj)  # Create order item (course obj)

        # Save order id via session
        request.session['order_id'] = order.oid
        request.session.modified = True

        return redirect('payment:create_bank')


# Add Course view
class AddCourseView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
        if not tracking_code:
            return redirect('payment:callback_failed')

        try:
            bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
        except bank_models.Bank.DoesNotExist:
            return redirect('payment:callback_failed')

        if not bank_record.is_success:
            return redirect('payment:callback_failed')

        return super(AddCourseView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        try:
            order = Order.objects.get(oid=request.session['order_id'])
            order_items = OrderItem.objects.filter(order=order)
        except (Order.DoesNotExist, KeyError):
            raise Http404

        # Add new course to user courses
        for item in order_items:
            UserCourse.objects.create(user=order.user, course=item.item_object)

        # Add bank tracking code to order
        tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
        order.bank_tracking_code = tracking_code
        order.save()

        return redirect('payment:callback_success')
