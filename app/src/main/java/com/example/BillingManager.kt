package com.example

import android.app.Activity
import android.content.Context
import android.widget.Toast
import com.android.billingclient.api.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class BillingManager(private val context: Context) : PurchasesUpdatedListener {
    private var billingClient: BillingClient
    private val pendingCallbacks = mutableMapOf<String, () -> Unit>()

    private val _productDetails = MutableStateFlow<Map<String, ProductDetails>>(emptyMap())
    val productDetails: StateFlow<Map<String, ProductDetails>> = _productDetails.asStateFlow()

    init {
        billingClient = BillingClient.newBuilder(context)
            .setListener(this)
            .enablePendingPurchases()
            .build()
            
        startConnection()
    }

    private fun startConnection() {
        billingClient.startConnection(object : BillingClientStateListener {
            override fun onBillingSetupFinished(billingResult: BillingResult) {
                if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
                    queryAvailableProducts()
                    restorePurchases()
                }
            }
            override fun onBillingServiceDisconnected() {
                // Retry connection in a real production environment
            }
        })
    }
    
    private val _restoredPurchases = MutableStateFlow<Set<String>>(emptySet())
    val restoredPurchases: StateFlow<Set<String>> = _restoredPurchases.asStateFlow()

    private fun restorePurchases() {
        val params = QueryPurchasesParams.newBuilder()
            .setProductType(BillingClient.ProductType.INAPP)
            .build()
            
        billingClient.queryPurchasesAsync(params) { billingResult, purchases ->
            if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
                val ownedProducts = mutableSetOf<String>()
                for (purchase in purchases) {
                    if (purchase.purchaseState == Purchase.PurchaseState.PURCHASED) {
                        ownedProducts.addAll(purchase.products)
                        if (!purchase.isAcknowledged) {
                            acknowledgePurchase(purchase)
                        }
                    }
                }
                _restoredPurchases.value = ownedProducts
            }
        }
    }

    private fun queryAvailableProducts() {
        val productList = listOf(
            QueryProductDetailsParams.Product.newBuilder()
                .setProductId("coin_pack_1000")
                .setProductType(BillingClient.ProductType.INAPP)
                .build(),
            QueryProductDetailsParams.Product.newBuilder()
                .setProductId("coin_pack_5000")
                .setProductType(BillingClient.ProductType.INAPP)
                .build(),
            QueryProductDetailsParams.Product.newBuilder()
                .setProductId("coin_pack_12000")
                .setProductType(BillingClient.ProductType.INAPP)
                .build(),
            QueryProductDetailsParams.Product.newBuilder()
                .setProductId("remove_ads")
                .setProductType(BillingClient.ProductType.INAPP)
                .build()
        )

        val params = QueryProductDetailsParams.newBuilder()
            .setProductList(productList)
            .build()

        billingClient.queryProductDetailsAsync(params) { billingResult, productDetailsList ->
            if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
                val map = productDetailsList.associateBy { it.productId }
                _productDetails.value = map
            }
        }
    }

    fun initiatePurchaseFlow(activity: Activity, productId: String, onSuccess: () -> Unit) {
        val productDetail = _productDetails.value[productId]
        if (productDetail != null) {
            pendingCallbacks[productId] = onSuccess
            
            val productDetailsParamsList = listOf(
                BillingFlowParams.ProductDetailsParams.newBuilder()
                    .setProductDetails(productDetail)
                    .build()
            )
            val billingFlowParams = BillingFlowParams.newBuilder()
                .setProductDetailsParamsList(productDetailsParamsList)
                .build()
                
            billingClient.launchBillingFlow(activity, billingFlowParams)
        } else {
            Toast.makeText(context, "Product not available", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onPurchasesUpdated(billingResult: BillingResult, purchases: MutableList<Purchase>?) {
        if (billingResult.responseCode == BillingClient.BillingResponseCode.OK && purchases != null) {
            for (purchase in purchases) {
                handlePurchase(purchase)
            }
        }
    }

    private fun handlePurchase(purchase: Purchase) {
        if (purchase.purchaseState == Purchase.PurchaseState.PURCHASED) {
            val isConsumable = purchase.products.any { it.startsWith("coin_pack") }
            
            if (isConsumable) {
                val consumeParams = ConsumeParams.newBuilder()
                    .setPurchaseToken(purchase.purchaseToken)
                    .build()
    
                CoroutineScope(Dispatchers.Main).launch {
                    val consumeResult = billingClient.consumePurchase(consumeParams)
                    if (consumeResult.billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
                        for (productId in purchase.products) {
                            pendingCallbacks[productId]?.invoke()
                            pendingCallbacks.remove(productId)
                        }
                        Toast.makeText(context, "Purchase Successful!", Toast.LENGTH_SHORT).show()
                    } else {
                        Toast.makeText(context, "Error consuming purchase", Toast.LENGTH_SHORT).show()
                    }
                }
            } else {
                if (!purchase.isAcknowledged) {
                    acknowledgePurchase(purchase)
                } else {
                    for (productId in purchase.products) {
                        pendingCallbacks[productId]?.invoke()
                        pendingCallbacks.remove(productId)
                    }
                }
            }
        }
    }
    
    private fun acknowledgePurchase(purchase: Purchase) {
        val acknowledgePurchaseParams = AcknowledgePurchaseParams.newBuilder()
            .setPurchaseToken(purchase.purchaseToken)
            .build()
        
        CoroutineScope(Dispatchers.Main).launch {
            val ackResult = billingClient.acknowledgePurchase(acknowledgePurchaseParams)
            if (ackResult.responseCode == BillingClient.BillingResponseCode.OK) {
                for (productId in purchase.products) {
                    pendingCallbacks[productId]?.invoke()
                    pendingCallbacks.remove(productId)
                }
                Toast.makeText(context, "Purchase Successful!", Toast.LENGTH_SHORT).show()
            }
        }
    }
}
