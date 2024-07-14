from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.templatetags.static import static
from django.shortcuts import reverse
from django.db import models

from apps.core.models import BaseModel

User = get_user_model()


# MyRestaurant model
class Restaurant(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurants', verbose_name=_('User'))
    code = models.PositiveIntegerField(_('Code'), null=True, blank=True)
    title = models.CharField(_('Title'), max_length=128, default=_('No title'))
    services_fee = models.PositiveSmallIntegerField(_('Services fee'), default=5)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Restaurant')
        verbose_name_plural = _('Restaurants')

    def __str__(self):
        return f'{self.user} - {self.user.profile.place_name}'

    def get_material_categories(self):
        return self.raw_material_categories.filter(is_active=True)

    def get_recipes_categories(self):
        return self.recipes_categories.all()

    def get_prepared_material_categories(self):
        return self.prepared_material_categories.all()


# ----------------------------------------------------------------------


# RawMaterialCategories model
class RawMaterialCategory(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='raw_material_categories',
                                   verbose_name=_('Restaurant'))
    title = models.CharField(_('Title'), max_length=128, default=_('Test category'))
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Raw materials category')
        verbose_name_plural = _('Raw materials categories')

    def __str__(self):
        return f'{self.restaurant} - {self.title}'

    def get_materials(self):
        return self.raw_materials.all()


# RawMaterials model
class RawMaterial(BaseModel):
    category = models.ForeignKey(RawMaterialCategory, on_delete=models.CASCADE, related_name='raw_materials',
                                 verbose_name=_('Category'))

    # Common info
    title = models.CharField(_('Title'), max_length=128)
    price = models.PositiveIntegerField(_('Price'), default=0, help_text=_('Per unit'))
    use_for = models.CharField(_('Use for'), max_length=128, null=True, blank=True)
    quantity_raw_press = models.DecimalField(_('Standard quantity per raw press'), max_digits=5, decimal_places=3,
                                             default=0)
    quantity_baked_press = models.DecimalField(_('Standard quantity per baked press'), max_digits=5, decimal_places=3,
                                               default=0)
    delivery_weight = models.DecimalField(_('Delivery weight'), max_digits=5, decimal_places=2, default=0)

    # Weight loss during cleaning info
    weight_loss_cleaning_usable = models.DecimalField(_('Weight loss due to cleaning(usable)'), max_digits=4,
                                                      decimal_places=2, default=0)
    weight_loss_cleaning_unusable = models.DecimalField(_('Weight loss due to cleaning(unusable)'), max_digits=4,
                                                        decimal_places=2, default=0)
    edible_cleaned_weight = models.DecimalField(_('Edible cleaned weight'), max_digits=5, decimal_places=2, default=0)

    # Weight loss during baking info
    weight_loss_baking = models.DecimalField(_('Weight loss due to baking'), max_digits=4, decimal_places=2, default=0)
    salable_weight = models.DecimalField(_('Salable weight(usable)'), max_digits=5, decimal_places=2, default=0)

    # Computational ratios of yield test
    raw_usable_quantity_cost = models.PositiveIntegerField(_('Cost of raw usable quantity'), default=0)
    baked_usable_quantity_cost = models.PositiveIntegerField(_('Cost of baked usable quantity'), default=0)
    raw_usable_quantity_cost_per_press = models.PositiveIntegerField(_('Cost of raw usable quantity per press'),
                                                                     default=0)
    baked_usable_quantity_cost_per_press = models.PositiveIntegerField(_('Cost of baked usable quantity per press'),
                                                                       default=0)
    number_of_raw_use = models.PositiveIntegerField(_('Number of raw use'), default=0)
    number_of_baked_use = models.PositiveIntegerField(_('Number of baked use'), default=0)

    class Meta:
        verbose_name = _('Raw material')
        verbose_name_plural = _('Raw materials')

    def __str__(self):
        return f'{self.title} {self.get_use_for()}'

    def save(self, *args, **kwargs):
        self.calculate_results()
        super().save(*args, **kwargs)

    def calculate_results(self):
        """ Calculate obj usable things and save them. """
        if self.delivery_weight and self.edible_cleaned_weight:
            self.raw_usable_quantity_cost = (self.price * self.delivery_weight) / self.edible_cleaned_weight
        else:
            self.raw_usable_quantity_cost = self.price

        if self.delivery_weight and self.salable_weight:
            self.baked_usable_quantity_cost = (self.price * self.delivery_weight) / self.salable_weight

        self.raw_usable_quantity_cost_per_press = self.raw_usable_quantity_cost * self.quantity_raw_press
        self.baked_usable_quantity_cost_per_press = self.raw_usable_quantity_cost * self.quantity_baked_press

        self.number_of_raw_use = self.edible_cleaned_weight / self.quantity_raw_press if self.quantity_raw_press else 0
        self.number_of_baked_use = self.salable_weight / self.quantity_baked_press if self.quantity_baked_press else 0

    def get_reduce_form_url(self):
        return reverse('restaurant:raw_materials_reduce_form', args=[self.pk])

    def get_use_for(self):
        return f'({self.use_for})' if self.use_for else ''


# ------------------------------------------------------------------------------------


# RecipesCategories model
class RecipesCategory(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='recipes_categories',
                                   verbose_name=_('Restaurant'))
    title = models.CharField(_('Title'), max_length=128, default=_('No title'))

    class Meta:
        verbose_name = _('Food recipes category')
        verbose_name_plural = _('Food recipes categories')

    def __str__(self):
        return f'{self.restaurant} - {self.title}'

    def get_recipes(self):
        return self.recipes.filter(is_active=True)


# PreparedMaterialCategories model
class PreparedMaterialCategory(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='prepared_material_categories',
                                   verbose_name=_('Restaurant'))
    title = models.CharField(_('Title'), max_length=128, default=_('No title'))

    class Meta:
        verbose_name = _('Prepared material category')
        verbose_name_plural = _('Prepared material categories')

    def __str__(self):
        return f'{self.restaurant} - {self.title}'

    def get_recipes(self):
        return self.material_recipes.filter(is_active=True)


# Recipes model
class Recipe(BaseModel):
    category = models.ForeignKey(RecipesCategory, on_delete=models.CASCADE, related_name='recipes',
                                 verbose_name=_('Category'), null=True, blank=True)
    prepared_category = models.ForeignKey(PreparedMaterialCategory, on_delete=models.CASCADE,
                                          related_name='material_recipes', verbose_name=_('Prepared category'),
                                          null=True, blank=True)
    title = models.CharField(_('Title'), max_length=128, default=_('No title'))
    preparation = models.TextField(_('How to prepare'), null=True, blank=True)

    final_price = models.PositiveIntegerField(_('Final price'), default=0)
    factor = models.DecimalField(_('Factor coefficient'), max_digits=3, decimal_places=1, default=1.5)  # User input
    service_price = models.PositiveIntegerField(_('Services price'), default=0)  # final_price * (services_fee / 100)
    price_with_factor = models.PositiveIntegerField(_('Final price with factor'), default=0)  # final_price * factor
    menu_price = models.PositiveIntegerField(_('Menu price'), default=0)  # User input
    item_profit = models.IntegerField(_('Item profit'), default=0)  # menu_price - servie_price - final_price
    food_cost = models.IntegerField(_('Food cost'), default=0)  # (final_price / menu_price) * 100
    number_sold = models.PositiveIntegerField(_('Number sold'), default=0)  # User input
    total_sales = models.BigIntegerField(_('Total sales'), default=0)  # number_sold * menu_price
    total_cost = models.BigIntegerField(_('Total cost'), default=0)  # number_sold * final_price
    total_profit = models.BigIntegerField(_('Total profit'), default=0)  # number_sold * item_profit

    image = models.ImageField(_('Image'), upload_to='images/recipes/', null=True, blank=True)
    is_material = models.BooleanField(_('Is material'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Food recipe')
        verbose_name_plural = _('Food recipes')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('restaurant:recipe_details', args=[self.pk])

    def get_preparation_url(self):
        return reverse('restaurant:preparation_details', args=[self.pk])

    def get_image_url(self):
        if self.image:
            return self.image.url
        return static('images/logo-yellow.png')

    def get_materials(self):
        return self.materials.all()

    def get_prepared_materials(self):
        return self.prepared_materials.all()

    def calc_final_price(self, calc_others=True):
        materials = self.materials.all()
        price = sum(map(lambda m: m.calc_final_price(), materials))

        # Save if final price has changed
        if self.final_price != price:
            self.final_price = price

            # Calculate other things if it's allowed
            if calc_others:
                self.calculate_results(save=False)
            self.save()

        return price

    def calculate_results(self, save=True):
        self.calc_final_price(calc_others=False)

        # Calculate services_price
        if self.category:
            self.service_price = self.final_price * (self.category.restaurant.services_fee / 100)
        else:
            self.service_price = self.final_price * (self.prepared_category.restaurant.services_fee / 100)

        self.price_with_factor = int(self.final_price * self.factor) + self.service_price  # Calculate price_with_factor
        if self.menu_price:
            self.item_profit = self.menu_price - self.service_price - self.final_price  # Calculate item_profit
            self.food_cost = (self.final_price / self.menu_price) * 100  # Calculate food_cost
            self.total_sales = self.number_sold * self.menu_price  # Calculate total_sales
            self.total_cost = self.number_sold * self.final_price  # Calculate total_cost
            self.total_profit = self.number_sold * self.item_profit  # Calculate total_profit

        if save:
            self.save()


# RecipeMaterials model
class RecipeMaterial(BaseModel):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='materials', verbose_name=_('Recipe'))
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, related_name='recipe_materials',
                                     verbose_name=_('Raw material'), null=True, blank=True)
    prepared_material = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='prepared_materials',
                                          verbose_name=_('Prepared material'), null=True, blank=True)
    amount = models.DecimalField(_('Amount'), max_digits=7, decimal_places=3, default=0)
    final_price = models.PositiveIntegerField(_('Final price'), default=0)

    class Meta:
        verbose_name = _('Recipe material')
        verbose_name_plural = _('Recipe materials')

    def __str__(self):
        return f'{self.recipe} - {self.raw_material or self.prepared_material}'

    def save(self, *args, **kwargs):
        self.calc_final_price(save=False)
        super().save(*args, **kwargs)

    def get_base_price(self):
        if self.prepared_material:
            return self.prepared_material.final_price
        elif self.raw_material:
            return self.raw_material.raw_usable_quantity_cost

    def get_material_title(self):
        return self.prepared_material or self.raw_material

    def calc_final_price(self, save=True):
        if self.prepared_material:
            final_price = int(self.amount * self.prepared_material.final_price)
        else:
            final_price = int(self.amount * self.raw_material.raw_usable_quantity_cost)

        if save and final_price != self.final_price:
            self.final_price = final_price
            self.save()

        return final_price


class RestaurantProfile(BaseModel):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE, verbose_name=_('User'), )
    initial_investment = models.PositiveBigIntegerField(_('Initial investment'))
    cost_of_raw_materials = models.PositiveBigIntegerField(_('Cost raw materials'))
    food_cost = models.SmallIntegerField(_('Food cost'))  # by percent
    tax = models.SmallIntegerField(_('Tax'), default=0)  # by percent

    class Meta:
        verbose_name = _('Restaurant profile')
        verbose_name_plural = _('Restaurant profiles')

    def __str__(self):
        return f'restaurant profile {self.user}'

    def get_fixed_costs(self):
        return self.fixedcosts_set.all().order_by('-price')

    def get_fixed_costs_price(self):
        return self.get_fixed_costs().aggregate(total=models.Sum('price'))['total'] or 0

    def get_fixed_costs_total_price(self):
        return self.get_fixed_costs_price() + self.cost_of_raw_materials

    def get_ongoing_costs(self):
        return self.ongoingcosts_set.all().order_by('-price')

    def get_ongoing_costs_total_price(self):
        return self.get_ongoing_costs().aggregate(total=models.Sum('price'))['total'] or 0

    def get_income_and_costs(self):
        return self.incomeandcostsprofile_set.all()

    def get_sales_estimate_total(self):
        # TODO: better to use DB functions for calc
        total = 0
        for i in self.get_income_and_costs():
            total += i.get_sales_estimate()
        return total

    def get_raw_materials_estimate_total(self):
        # TODO: better to use DB functions for calc
        total = 0
        for i in self.get_income_and_costs():
            total += i.get_raw_materials_estimate()
        return total

    def get_profit_estimate_total(self):
        # TODO: better to use DB functions for calc
        total = 0
        for i in self.get_income_and_costs():
            total += i.get_profit_estimate()
        return total

    def get_profit_with_tax_estimate_total(self):
        # TODO: better to use DB functions for calc
        total = 0
        for i in self.get_income_and_costs():
            total += i.get_profit_with_tax_estimate()
        return total

    def get_profit_with_tax_estimate_avg(self):
        # TODO: better to use DB functions for calc
        total = 0
        incomes = self.get_income_and_costs()
        for i in incomes:
            total += i.get_profit_with_tax_estimate()
        return (total / incomes.count())

    def get_p2p_sales(self):
        r = (self.get_ongoing_costs_total_price() * 100) / (100 - self.food_cost)
        return int(r)

    def get_p2p_fill_seats(self):
        last_income = self.get_income_and_costs().first()
        if not last_income:
            return None
        r = (self.get_p2p_sales() / (
                last_income.duration * last_income.number_of_seats * last_income.avg_purchase)) * 100
        return int(r)

    def get_return_of_investment(self):
        r = self.get_fixed_costs_total_price() / self.get_profit_with_tax_estimate_avg()
        return int(r)


class FixedCosts(BaseModel):
    restaurant_profile = models.ForeignKey('RestaurantProfile', on_delete=models.CASCADE,
                                           verbose_name=_('Restaurant profile'))
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), null=True, blank=True)
    price = models.PositiveIntegerField(_('Price'))

    def __str__(self):
        return self.name


class OngoingCosts(BaseModel):
    restaurant_profile = models.ForeignKey('RestaurantProfile', on_delete=models.CASCADE,
                                           verbose_name=_('Restaurant profile'))
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), null=True, blank=True)
    price = models.PositiveIntegerField(_('Price'))

    def __str__(self):
        return self.name


class IncomeAndCostsProfile(BaseModel):
    restaurant_profile = models.ForeignKey('RestaurantProfile', on_delete=models.CASCADE,
                                           verbose_name=_('Restaurant profile'))
    duration = models.SmallIntegerField()  # by day
    number_of_seats = models.SmallIntegerField()
    avg_purchase = models.PositiveIntegerField()
    avg_seat_occupancy = models.SmallIntegerField()  # by percent

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'{self.restaurant_profile} income and costs'

    def get_sales_estimate(self):
        r = (self.duration * self.number_of_seats * self.avg_purchase * self.avg_seat_occupancy) / 100
        return r

    def get_raw_materials_estimate(self):
        sales = self.get_sales_estimate()
        return (sales / 100) * self.restaurant_profile.food_cost

    def get_profit_estimate(self):
        costs = self.get_raw_materials_estimate() + self.restaurant_profile.get_ongoing_costs_total_price()
        profit = self.get_sales_estimate() - costs
        return profit

    def get_profit_with_tax_estimate(self):
        tax = self.restaurant_profile.tax
        profit_without_tax = self.get_profit_estimate()
        profit_with_tax = profit_without_tax - ((profit_without_tax / 100) * tax)
        return profit_with_tax
