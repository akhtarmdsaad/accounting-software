function round(number,digits=2){
  var decimal = number * Math.pow(10,digits)
  decimal = Math.round(decimal) / 100
  return(decimal)
}

invoice_no_input = document.getElementById("invoice_no")
date_input = document.getElementById("date")
cust_sel = document.querySelector("#customers_select")
// sessionStorage.setItem('cust_sel','Select Customer') 

function update_random_customer(case_no)
{
  // 3 cases in total

  // 1. Customer is cash 
  // 2. Customer has to enter shipping address 
  // 3 (else). Customer doesnt need any of that

  node = document.querySelector(".random_customer")
  checkbox = document.querySelector(".change_shipping_address") 
  checkbox_input = document.querySelector("input #change_shipping_address") 
  customer_name = document.getElementById("shipping_customer_name")
  address = document.getElementById("shipping_address")
  state = document.getElementById("shipping_state")
  
  if(case_no == 1)
  {
    node.style.display="block"
    checkbox.style.display="none"
    
    data = sessionStorage.getItem('customer_name') 
    if(data)
      customer_name.value = data;  
    
    data = sessionStorage.getItem('address') 
    if(data)
      address.value = data;
    
    data = sessionStorage.getItem('state') 
    if(data)
      state.value = data
      

    customer_name.addEventListener('input',(e)=>{
      sessionStorage.setItem('customer_name',customer_name.value) 
    });
    
    address.addEventListener('input',(e)=>{
      sessionStorage.setItem('address',address.value) 
    });
    
    state.addEventListener('change',(e)=>{
      sessionStorage.setItem('state',state.value) 
    });

    // add the required role here
    customer_name.setAttribute("required",true) 
    address.setAttribute("required",true) 

  }
  else if(case_no == 2)
  {
    node.style.display="block" 
    
    data = sessionStorage.getItem("checked_shipping")
    if(data && checkbox_input)
      checkbox_input.checked = true;
    
    data = sessionStorage.getItem('customer_name') 
    if(data)
      customer_name.value = data;  
    
    data = sessionStorage.getItem('address') 
    if(data)
      address.value = data;
    
    data = sessionStorage.getItem('state') 
    if(data)
      state.value = data;
      

    customer_name.addEventListener('input',(e)=>{
      sessionStorage.setItem('customer_name',customer_name.value) 
    });
    
    address.addEventListener('input',(e)=>{
      sessionStorage.setItem('address',address.value) 
    });
    
    state.addEventListener('change',(e)=>{
      sessionStorage.setItem('state',state.value) 
    });

    customer_name.setAttribute("required",true) 
    address.setAttribute("required",true) 
  }
  else
  {
    node.style.display = "none"
    checkbox.style.display = "block"

    data = sessionStorage.getItem("checked_shipping")
    if(data && checkbox_input)
      checkbox_input.checked = true

    customer_name.removeAttribute("required") 
    address.removeAttribute("required")

    customer_name.removeEventListener('input',(e)=>{
      sessionStorage.setItem('customer_name',customer_name.value) 
    });
    
    address.removeEventListener('input',(e)=>{
      sessionStorage.setItem('address',address.value) 
    });
    
    state.removeEventListener('change',(e)=>{
      sessionStorage.setItem('state',state.value) 
    });
  }
} // closed update input random customer

checkbox = document.getElementById("change_shipping_address")
checkbox.addEventListener("change",(e)=>{
  if(e.target.checked)
  {
    update_random_customer(2)
  }
  else 
  {
    update_random_customer(3)
  }
  sessionStorage.setItem("checked_shipping",e.target.checked)
})

add_item_button = document.getElementById("add_item")
edit_transaction_button = document.getElementById("edit_transaction_button")

data = sessionStorage.getItem('invoice_no') 
if(data)
  invoice_no_input.value = data;

data = sessionStorage.getItem('cust_sel') 
if(data)
{
  cust_sel.value = data;
  customer_id_in_transaction.value = data
  customer_id_in_transaction2.value = data
}
data = sessionStorage.getItem('date') 
if(data)
  date_input.value = data;



document.getElementById("reset").addEventListener("click",(e)=>{
  sessionStorage.clear()
  customer_id_in_transaction.value = "2"
  customer_id_in_transaction2.value = "2"
})

// session storage
invoice_no_input.addEventListener('input',(e)=>{
  sessionStorage.setItem('invoice_no',document.getElementById("invoice_no").value) 
});

date_input.addEventListener('input',(e)=>{
  sessionStorage.setItem('date',document.getElementById("date").value) 
});


qnt = document.querySelector("#modal-form #qnt")
qnt2 = document.querySelector("#modal-form2 #qnt2")

rate = document.querySelector("#modal-form #rate")
rate2 = document.querySelector("#modal-form2 #rate2")

taxable_value = document.querySelector("#modal-form #taxable_value")
taxable_value2 = document.querySelector("#modal-form2 #taxable_value2")

discount_percent = document.querySelector("#modal-form #discount_percent")
discount_percent2 = document.querySelector("#modal-form2 #discount_percent2")

discount_amount = document.querySelector("#modal-form #discount_amount")
discount_amount2 = document.querySelector("#modal-form2 #discount_amount2")

total_rate = document.querySelector("#modal-form #total_rate")
total_rate2 = document.querySelector("#modal-form2 #total_rate2")

total_amount = document.querySelector("#modal-form #total_amount")
total_amount2 = document.querySelector("#modal-form2 #total_amount2")

tax_button = document.querySelector("#modal-form #tax")
tax_button2 = document.querySelector("#modal-form2 #tax2")

current_stock_button = document.querySelector("#modal-form #current_stock")
current_stock_button2 = document.querySelector("#modal-form2 #current_stock2")

item = document.querySelector("#modal-form #item")
item2 = document.querySelector("#modal-form2 #item2")
// tax_button.value = item.selectedOptions[0].getAttribute('tax');
// current_stock_button.value = item.selectedOptions[0].getAttribute('current_stock');
// {% comment %} item.onclick = (e)=>{
//   tax_button.value = item.selectedOptions[0].getAttribute('tax');
//   current_stock_button.value = item.selectedOptions[0].getAttribute('current_stock');

// }; {% endcomment %}

qnt.setAttribute("min",0);
qnt.setAttribute("max",0);
qnt2.setAttribute("min",0);
qnt2.setAttribute("max",0);


qnt.addEventListener("input",(e)=>{
  qnt_no = qnt.value;
  if(qnt_no){
    taxable_value.value = round(rate.value * qnt_no,2);
    total_amount.value = round( ((taxable_value.value-discount_amount.value) * (1 + (tax_button.value*2)/100)),2);
    total_rate.value = round( total_amount.value / qnt_no,2);
  }
  else{
    taxable_value.value =  0
    total_amount.value = 0
    total_rate.value = 0
  }
}); 
qnt2.addEventListener("input",(e)=>{
  qnt_no = qnt2.value;
  if(qnt_no){
    taxable_value2.value = round(rate2.value * qnt_no,2);
    total_amount2.value = round( ((taxable_value2.value-discount_amount2.value) * (1 + (tax_button2.value*2)/100)),2);
    total_rate2.value = round( total_amount2.value / qnt_no,2);
  }
  else{
    taxable_value2.value =  0
    total_amount2.value = 0
    total_rate2.value = 0
  }
}); 

discount_percent.addEventListener("input",(e)=>{
  if(discount_percent.value){
    discount_amount.value =round( taxable_value.value * discount_percent.value / 100,2);
    total_amount.value = round( ((taxable_value.value-discount_amount.value) * (1 + (tax_button.value*2)/100)),2);
    total_rate.value = round( total_amount.value / qnt.value,2);
  }
  else
  {
    discount_amount.value = 0
    total_amount.value = round( ((taxable_value.value-discount_amount.value) * (1 + (tax_button.value*2)/100)),2);
    total_rate.value = round( total_amount.value / qnt.value,2);
  }
})
discount_percent2.addEventListener("input",(e)=>{
  if(discount_percent2.value){
    discount_amount2.value =round( taxable_value2.value * discount_percent2.value / 100,2);
    total_amount2.value = round( ((taxable_value2.value-discount_amount2.value) * (1 + (tax_button2.value*2)/100)),2);
    total_rate2.value = round( total_amount2.value / qnt2.value,2);
  }
  else
  {
    discount_amount2.value = 0
    total_amount2.value = round( ((taxable_value2.value-discount_amount2.value) * (1 + (tax_button2.value*2)/100)),2);
    total_rate2.value = round( total_amount2.value / qnt2.value,2);
  }
})

discount_amount.addEventListener("input",(e)=>{
  if(discount_amount.value){
    discount_percent.value = round( discount_amount.value * 100 / taxable_value.value,2);
    total_amount.value = round( ((taxable_value.value-discount_amount.value) * (1 + (tax_button.value*2)/100)),2);
    total_rate.value = round( total_amount.value / qnt.value,2);
  }
  else
  {
    discount_percent.value = 0
    total_amount.value = round( ((taxable_value.value-discount_amount.value) * (1 + (tax_button.value*2)/100)),2);
    total_rate.value = round( total_amount.value / qnt.value,2);
  }
})

discount_amount2.addEventListener("input",(e)=>{
  if(discount_amount2.value){
    discount_percent2.value = round( discount_amount2.value * 100 / taxable_value2.value,2);
    total_amount2.value = round( ((taxable_value2.value-discount_amount2.value) * (1 + (tax_button2.value*2)/100)),2);
    total_rate2.value = round( total_amount2.value / qnt2.value,2);
  }
  else
  {
    discount_percent2.value = 0
    total_amount2.value = round( ((taxable_value2.value-discount_amount2.value) * (1 + (tax_button2.value*2)/100)),2);
    total_rate2.value = round( total_amount2.value / qnt2.value,2);
  }
})

rate.addEventListener("input",(e)=>{
  qnt_no = qnt.value;
  if(rate.value){
    taxable_value.value = round(  rate.value * qnt_no,2);
    total_amount.value = round( ((taxable_value.value-discount_amount.value) * (1 + (tax_button.value*2)/100)),2);
    total_rate.value = round( total_amount.value / qnt_no,2);
  }
  else{
    taxable_value.value =  0
    total_amount.value = 0
    total_rate.value = 0
  }
}); 
rate2.addEventListener("input",(e)=>{
  qnt_no = qnt2.value;
  if(rate2.value){
    taxable_value2.value = round(  rate2.value * qnt_no,2);
    total_amount2.value = round( ((taxable_value2.value-discount_amount2.value) * (1 + (tax_button2.value*2)/100)),2);
    total_rate2.value = round( total_amount2.value / qnt_no,2);
  }
  else{
    taxable_value2.value =  0
    total_amount2.value = 0
    total_rate2.value = 0
  }
}); 

taxable_value.addEventListener("input",(e)=>{
  qnt_no = qnt.value;
  if(taxable_value.value){
    rate.value = round( taxable_value.value / qnt_no,2);
    total_amount.value = round( ((taxable_value.value-discount_amount.value) * (1 + (tax_button.value*2)/100)),2);
    total_rate.value = round( total_amount.value / qnt_no,2);
  }
  else{
    rate.value=0
    total_amount.value = 0
    total_rate.value = 0
  } 
});
taxable_value2.addEventListener("input",(e)=>{
  qnt_no = qnt2.value;
  if(taxable_value2.value){
    rate2.value = round( taxable_value2.value / qnt_no,2);
    total_amount2.value = round( ((taxable_value2.value-discount_amount2.value) * (1 + (tax_button2.value*2)/100)),2);
    total_rate2.value = round( total_amount2.value / qnt_no,2);
  }
  else{
    rate2.value=0
    total_amount2.value = 0
    total_rate2.value = 0
  } 
});

total_amount.addEventListener("input",(e)=>{
  qnt_no = qnt.value;
  if(total_amount.value){
    if(!discount_percent.value){
      discount_percent.value = 0
    }
    taxable_value.value = round( (total_amount.value / (1 + (tax_button.value*2)/100)) / (1 - (discount_percent.value/100)),2);
    discount_amount.value = round( taxable_value.value * discount_percent.value / 100,2);
    rate.value = round( parseFloat(taxable_value.value) / qnt_no,2);
    total_rate.value = round( total_amount.value / qnt_no,2);
  }
  else{
    rate.value=0
    taxable_value.value =  0
    total_rate.value = 0
  }
});
total_amount2.addEventListener("input",(e)=>{
  qnt_no = qnt2.value;
  if(total_amount2.value){
    if(!discount_percent2.value){
      discount_percent2.value = 0
    }
    taxable_value2.value = round( (total_amount2.value / (1 + (tax_button2.value*2)/100)) / (1 - (discount_percent2.value/100)),2);
    discount_amount2.value = round( taxable_value2.value * discount_percent2.value / 100,2);
    rate2.value = round( parseFloat(taxable_value2.value) / qnt_no,2);
    total_rate2.value = round( total_amount2.value / qnt_no,2);
  }
  else{
    rate2.value=0
    taxable_value2.value =  0
    total_rate2.value = 0
  }
});

total_rate.addEventListener("input",(e)=>{
  qnt_no = qnt.value;
  if(total_rate.value){
    total_amount.value = round( total_rate.value * qnt_no,2);
    taxable_value.value = round( (total_amount.value / (1 + (tax_button.value*2)/100)) / (1 - (discount_percent.value/100)),2);
    discount_amount.value = round( taxable_value.value * discount_percent.value / 100,2);
    rate.value = round( parseFloat(taxable_value.value) / qnt_no,2);
  }
  else{
    rate.value=0
    taxable_value.value =  0
    total_amount.value = 0
  }
});
total_rate2.addEventListener("input",(e)=>{
  qnt_no = qnt2.value;
  if(total_rate2.value){
    total_amount2.value = round( total_rate2.value * qnt_no,2);
    taxable_value2.value = round( (total_amount2.value / (1 + (tax_button2.value*2)/100)) / (1 - (discount_percent2.value/100)),2);
    discount_amount2.value = round( taxable_value2.value * discount_percent2.value / 100,2);
    rate2.value = round( parseFloat(taxable_value2.value) / qnt_no,2);
  }
  else{
    rate2.value=0
    taxable_value2.value =  0
    total_amount2.value = 0
  }
});


// Third Party Changes 
customer_id_in_transaction = document.getElementById("customer_id_in_transaction")
 function fetchAvailableQuantity(itemId) {
  $.ajax({
    url: '/finance/get_available_quantity/',
    method: 'GET',
    data: { item_id: itemId, customer_id: customer_id_in_transaction.value },
    success: function(response) {
      // Handle the response and update the UI with the available quantity
      $('#current_stock').val(response.available_quantity);
      $('#tax').val(response.tax_percent);
      $('#rate').val(response.item_rate);
      if(current_stock_button.value) { val = current_stock_button.value }
      else { val=0 }
      qnt.setAttribute("max",val);

      $('#edit_item').attr('href','/finance/edit_items/'+response.item_id+'/')
    },
    error: function(xhr, status, error) {
      // Handle the error if needed
      console.error(error);
    }
  });
}
customer_id_in_transaction2 = document.getElementById("customer_id_in_transaction2")
 function fetchAvailableQuantity2(itemId) {
  $.ajax({
    url: '/finance/get_available_quantity/',
    method: 'GET',
    data: { item_id: itemId, customer_id: customer_id_in_transaction2.value },
    success: function(response) {
      // Handle the response and update the UI with the available quantity
      $('#current_stock2').val(response.available_quantity);
      $('#tax2').val(response.tax_percent);
      $('#rate2').val(response.item_rate);
      if(current_stock_button2.value) { val = current_stock_button2.value }
      else { val=0 }
      qnt2.setAttribute("max",val);

      $('#edit_item2').attr('href','/finance/edit_items/'+response.item_id+'/')
    },
    error: function(xhr, status, error) {
      // Handle the error if needed
      console.error(error);
    }
  });
}


let newRateValue = null;
function fetchIfCash(customerId) {
  $.ajax({
    url: '/finance/get_ifcash/',
    method: 'GET',
    data: { customerId: customerId },
    success: function(response) {
      node = document.querySelector(".random_customer");
      if(response.customer_is_cash == 1)
      {
        update_random_customer(1)
      }
      else
      {
        update_random_customer(3)
      }
    },
    error: function(xhr, status, error) {
      // Handle the error if needed
      console.error(error);
    }
  });
}

$(document).ready(function() {
  
  $('#items_select').selectize({
  onChange: function(value) {
    // Make an AJAX request to fetch the available quantity
    fetchAvailableQuantity(value);
    
    }
  });
  $('#items_select2').selectize({
  onChange: function(value) {
    // Make an AJAX request to fetch the available quantity
    fetchAvailableQuantity2(value);
    console.log(value)
    }
  });
  $('#items_select2')[0].selectize.setValue("2")
  


  

  $(function () {
    $("#customers_select").selectize({
      onChange: function(value) {
        // Make an AJAX request to fetch the available quantity
        fetchIfCash(value);
        sessionStorage.setItem('cust_sel',value) 
        customer_id_in_transaction.value = value
        customer_id_in_transaction2.value = value
        
        }
    });
  });
  
});
fetchIfCash(document.getElementById("customers_select").value);



// Get required values for the transaction edit using ajax function
function fetchTransactionDetails() {
$.ajax({
  url: '/finance/get_transaction_details/',
  method: 'GET',
  data: { transaction_id: edit_transaction_button.getAttribute("info"), customer_id: customer_id_in_transaction2.value },
  success: function(response) {
    newRateValue = response.rate;
    // Handle the response and update the UI with the available quantity
    $.when($('#items_select2')[0].selectize.setValue(response.item_id)).done(function (a)
    {
    $('#current_stock2').val(response.available_quantity);
    $('#tax2').val(response.tax_percent);
    if(current_stock_button2.value) { val = current_stock_button2.value }
    else { val=0 }
    qnt2.setAttribute("max",val);
    qnt2.value = response.qnt
    $('#rate2').val(response.rate);
    $('#taxable_value2').val(response.taxable_value);
    $('#discount_percent2').val(response.discount_percent);
    $('#discount_amount2').val(response.discount_amount);
    $('#total_amount2').val(response.amount);
    total_rate2.value = round( total_amount2.value / qnt2.value,2);
    $('#edit_item2').attr('href','/finance/edit_items/'+response.item_id+'/')
    });
  },
  error: function(xhr, status, error) {
    // Handle the error if needed
    console.error(error);
  }
});
}

edit_transaction_button.addEventListener("click",(e)=>{
e.preventDefault();
fetchTransactionDetails();
})

$(document).ajaxStop(function () {
if (newRateValue !== null) {
  $('#rate2').val(newRateValue);
  newRateValue = null; // Reset newRateValue after updating #rate2
}
});
