from .models import FinishedGoodsStock


def upsert_finished_goods_stock(company, form):
    stock, _ = FinishedGoodsStock.objects.update_or_create(
        warehouse=form.cleaned_data["warehouse"],
        product=form.cleaned_data["product"],
        defaults={"quantity_available": form.cleaned_data["quantity_available"]},
    )
    return stock

