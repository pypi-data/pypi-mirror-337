import pandas as pd
import numpy as np
from datetime import datetime, timezone

def wmOrdersReport(filePath:str):
    ordersDf = pd.read_excel(filePath)
    ordersDf = ordersDf.rename(columns=lambda x:x.replace(' ','_').replace('-','_').replace('#','').lower())

    ordersDf['order_date'] = pd.to_datetime(ordersDf['order_date'])
    ordersDf['delivery_date'] = pd.to_datetime(ordersDf['delivery_date'])
    ordersDf['service_scheduled_date'] = pd.to_datetime(ordersDf['service_scheduled_date'])

    req_columns = [
        'po',
        'service_po',
        'order',
        'order_date',
        'ship_by',
        'delivery_date',
        'service_scheduled_date',
        'customer_name',
        'customer_shipping_address',
        'customer_phone_number',
        'ship_to_address_1',
        'ship_to_address_2',
        'ship_to_country',
        'city',
        'state',
        'zip',
        'segment',
        'flids',
        'line',
        'upc',
        'status',
        'service_status',
        'item_description',
        'shipping_method',
        'shipping_tier',
        'shipping_sla',
        'shipping_config_source',
        'qty',
        'sku',
        'condition',
        'item_cost',
        'total_service_cost',
        'discount',
        'shipping_cost',
        'tax',
        'carrier',
        'tracking_number',
        'tracking_url',
        'update_status',
        'update_qty',
        'update_carrier',
        'update_tracking_number',
        'update_tracking_url',
        'seller_order_no',
        'fulfillment_entity',
        'replacement_order',
        'original_customer_order_id',
        'customer_intent_to_cancel',
        'intent_to_cancel_override',
        'platform_type'
    ]

    for col in req_columns:
        if col not in ordersDf.columns:
            ordersDf[col] = np.nan

    ordersDf = ordersDf[req_columns]

    schema = {
        'po': str,
        'service_po': str,
        'order': str,
        'order_date': 'datetime64[ns]',
        'ship_by': str,
        'delivery_date': 'datetime64[ns]',
        'service_scheduled_date': 'datetime64[ns]',
        'customer_name': str,
        'customer_shipping_address': str,
        'customer_phone_number': str,
        'ship_to_address_1': str,
        'ship_to_address_2': str,
        'ship_to_country': str,
        'city': str,
        'state': str,
        'zip': str,
        'segment': str,
        'flids': str,
        'line': str,
        'upc': str,
        'status': str,
        'service_status': str,
        'item_description': str,
        'shipping_method': str,
        'shipping_tier': str,
        'shipping_sla': float,
        'shipping_config_source': str,
        'qty': float,
        'sku': str,
        'condition': str,
        'item_cost': float,
        'total_service_cost': float,
        'discount': float,
        'shipping_cost': float,
        'tax': float,
        'carrier': str,
        'tracking_number': str,
        'tracking_url': str,
        'update_status': str,
        'update_qty': float,
        'update_carrier': str,
        'update_tracking_number': str,
        'update_tracking_url': str,
        'seller_order_no': str,
        'fulfillment_entity': str,
        'replacement_order': str,
        'original_customer_order_id': str,
        'customer_intent_to_cancel': str,
        'intent_to_cancel_override': str,
        'platform_type': str
    }

    ordersDf = ordersDf.astype(schema)

    return ordersDf

def wmAdsReport(filePath:str):
    adsDf = pd.read_csv(filePath, skiprows=1)
    adsDf = adsDf.rename(columns=lambda x:x.replace(' ','_').replace('(','').replace(')','').replace('#','').replace('-','').replace('.','').lower())
    adsDf['date'] = pd.to_datetime(adsDf['date'])
    adsDf = adsDf.replace({'\$':'',',':'','null':np.nan}, regex=True)

    req_columns = [
        'date',
        'item_id',
        'impressions',
        'clicks',
        'ad_spend',
        'total_units_sold__14_day',
        'advertised_sku_units__14_day',
        'other_sku_units___14_day',
        'orders__14_day',
        'total_sales_rev__14_day',
        'advertised_sku_sales__14_day',
        'other_sku_sales__14_day'
    ]

    missingColumns = set(req_columns) - set(adsDf.columns)
    newColumns = set(adsDf.columns) - set(req_columns)

    if missingColumns or newColumns:
        message = (
        f"""
        missing columns: {', '.join(missingColumns)}
        new columns: {', '.join(newColumns)}
        """
        )

        raise ValueError(message)

    adsDf = adsDf[req_columns]

    schema = {
        'date': 'datetime64[ns]',
        'item_id': str,
        'impressions': float,
        'clicks': float,
        'ad_spend': float,
        'total_units_sold__14_day': float,
        'advertised_sku_units__14_day': float,
        'other_sku_units___14_day': float,
        'orders__14_day': float,
        'total_sales_rev__14_day': float,
        'advertised_sku_sales__14_day': float,
        'other_sku_sales__14_day': float
    }

    adsDf = adsDf.astype(schema)

    return adsDf

def wmSettlementReport(filePath:str):
    settlementDf = pd.read_csv(filePath, skiprows=3)
    settlementDf = settlementDf.rename(columns=lambda x:x.replace(' ','_').replace('#','').replace('.','_').replace('/','_').lower())

    req_columns = [
        'walmart_com_order_',
        'walmart_com_order_line_',
        'walmart_com_po_',
        'walmart_com_po_line_',
        'transaction_type',
        'reason_code',
        'detail',
        'wfsreferenceid',
        'transaction_date_time',
        'qty',
        'partner_id',
        'partner_gtin',
        'partner_item_name',
        'category',
        'sub_category',
        'net_payable',
        'customerorderid',
        'orderchannelid'
    ]

    missingColumns = set(req_columns) - set(settlementDf.columns)
    newColumns = set(settlementDf.columns) - set(req_columns)

    if missingColumns or newColumns:
        message = (
        f"""
        missing columns: {', '.join(missingColumns)}
        new columns: {', '.join(newColumns)}
        """
        )

        raise ValueError(message)

    settlementDf = settlementDf[req_columns]
    settlementDf['transaction_date_time'] = pd.to_datetime(settlementDf['transaction_date_time'])

    schema = {
        'walmart_com_order_': str,
        'walmart_com_order_line_': float,
        'walmart_com_po_': str,
        'walmart_com_po_line_': float,
        'transaction_type': str,
        'reason_code': str,
        'detail': str,
        'wfsreferenceid': str,
        'transaction_date_time': 'datetime64[ns]',
        'qty': float,
        'partner_id': str,
        'partner_gtin': str,
        'partner_item_name': str,
        'category': str,
        'sub_category': str,
        'net_payable': float,
        'customerorderid': str,
        'orderchannelid': str
    }

    settlementDf = settlementDf.astype(schema)

    return settlementDf

def wmStorageReport(filePath:str):
    monthDf = pd.read_csv(filePath, skiprows=2)
    month = monthDf.columns[0]

    storageDf = pd.read_csv(filePath, skiprows=3)
    storageDf.insert(0, 'month', month)
    storageDf['month'] = pd.to_datetime(storageDf['month'])

    storageDf = storageDf.rename(columns=lambda x:x.replace(' ','_').replace('(','').replace(')','').replace('-','_').replace(',','').lower())

    req_columns = [
        'month',
        'partner_gtin',
        'vendor_sku',
        'walmart_item_id',
        'item_name',
        'length',
        'width',
        'height',
        'volume',
        'weight',
        'standard_daily_storage_cost_per_unit_off_peak_aged_under_365_days',
        'peak_daily_storage_cost_per_unit_aged_over_30_days',
        'long_term_daily_storage_cost_per_unit_aged_over_365_days',
        'average_units_on_hand',
        'ending_units_on_hand',
        'storage_fee_for_selected_time_period'
    ]

    missingColumns = set(req_columns) - set(storageDf.columns)
    newColumns = set(storageDf.columns) - set(req_columns)

    if missingColumns or newColumns:
        message = (
        f"""
        missing columns: {', '.join(missingColumns)}
        new columns: {', '.join(newColumns)}
        """
        )

        raise ValueError(message)

    schema = {
        'month': 'datetime64[ns]',
        'partner_gtin': str,
        'vendor_sku': str,
        'walmart_item_id': str,
        'item_name': str,
        'length': float,
        'width': float,
        'height': float,
        'volume': float,
        'weight': float,
        'standard_daily_storage_cost_per_unit_off_peak_aged_under_365_days': float,
        'peak_daily_storage_cost_per_unit_aged_over_30_days': float,
        'long_term_daily_storage_cost_per_unit_aged_over_365_days': float,
        'average_units_on_hand': float,
        'ending_units_on_hand': float,
        'storage_fee_for_selected_time_period': float
    }

    storageDf = storageDf.astype(schema)

    return storageDf

def wmAdGroupReport(filePath:str, reportDate:str):
    adsDf = pd.read_csv(filePath, skiprows=1)
    adsDf = adsDf.rename(columns=lambda x:x.replace(' ','_').replace('(','').replace(')','').replace('#','').replace('-','').replace('.','').lower())
    adsDf.insert(0, 'date', reportDate)
    adsDf = adsDf.replace({'\$':'',',':'','null':np.nan}, regex=True)

    req_columns = [
        'date',
        'ad_group_id',
        'ad_group_name',
        'item_id',
        'impressions',
        'clicks',
        'ad_spend',
        'total_units_sold__14_day',
        'advertised_sku_units__14_day',
        'other_sku_units___14_day',
        'orders__14_day',
        'total_sales_rev__14_day',
        'advertised_sku_sales__14_day',
        'other_sku_sales__14_day'
    ]

    missingColumns = set(req_columns) - set(adsDf.columns)
    newColumns = set(adsDf.columns) - set(req_columns)

    if missingColumns or newColumns:
        message = (
        f"""
        missing columns: {', '.join(missingColumns)}
        new columns: {', '.join(newColumns)}
        """
        )

        raise ValueError(message)

    adsDf = adsDf[req_columns]

    schema = {
        'date': 'datetime64[ns]',
        'ad_group_id': str,
        'ad_group_name': str,
        'item_id': str,
        'impressions': float,
        'clicks': float,
        'ad_spend': float,
        'total_units_sold__14_day': float,
        'advertised_sku_units__14_day': float,
        'other_sku_units___14_day': float,
        'orders__14_day': float,
        'total_sales_rev__14_day': float,
        'advertised_sku_sales__14_day': float,
        'other_sku_sales__14_day': float
    }

    adsDf = adsDf.astype(schema)
    return adsDf

def wmAdCampaignReport(filePath:str, reportDate:str):
    adsDf = pd.read_csv(filePath, skiprows=1)
    adsDf = adsDf.rename(columns=lambda x:x.replace(' ','_').replace('(','').replace(')','').replace('#','').replace('-','').replace('.','').lower())
    adsDf.insert(0, 'date', reportDate)
    adsDf = adsDf.replace({'\$':'',',':'','null':np.nan}, regex=True)

    req_columns = [
        'date',
        'campaign_name',
        'ad_group_id',
        'ad_group_name',
        'impressions',
        'clicks',
        'ad_spend',
        'total_units_sold__14_day',
        'advertised_sku_units__14_day',
        'other_sku_units___14_day',
        'orders__14_day',
        'total_sales_rev__14_day',
        'advertised_sku_sales__14_day',
        'other_sku_sales__14_day'
    ]

    missingColumns = set(req_columns) - set(adsDf.columns)
    newColumns = set(adsDf.columns) - set(req_columns)

    if missingColumns or newColumns:
        message = (
        f"""
        missing columns: {', '.join(missingColumns)}
        new columns: {', '.join(newColumns)}
        """
        )

        raise ValueError(message)

    adsDf = adsDf[req_columns]

    schema = {
        'date': 'datetime64[ns]',
        'campaign_name': str,
        'ad_group_id': str,
        'ad_group_name': str,
        'impressions': float,
        'clicks': float,
        'ad_spend': float,
        'total_units_sold__14_day': float,
        'advertised_sku_units__14_day': float,
        'other_sku_units___14_day': float,
        'orders__14_day': float,
        'total_sales_rev__14_day': float,
        'advertised_sku_sales__14_day': float,
        'other_sku_sales__14_day': float
    }

    adsDf = adsDf.astype(schema)
    return adsDf

