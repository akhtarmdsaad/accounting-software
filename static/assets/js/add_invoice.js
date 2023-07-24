function round(number,digits=2){
      var decimal = number * Math.pow(10,digits)
      decimal = Math.round(decimal) / 100
      return(decimal)
    }
  
    invoice_no_input = document.getElementById("invoice_no")
    date_input = document.getElementById("date")
    cust_sel = document.querySelector("#customers_select")
    // sessionStorage.setItem('cust_sel','Select Customer')  {% endcomment %}
  
    function update_input_cash()
    {
      customer_name = document.getElementsByName("customer_name")[0]
      address = document.getElementsByName("address")[0]
      if(!customer_name)
        return 0;
      data = sessionStorage.getItem('customer_name') 
      if(data)
        customer_name.value = data;  
      
      data = sessionStorage.getItem('address') 
      if(data)
        address.value = data;
  
      customer_name.addEventListener('input',(e)=>{
        sessionStorage.setItem('customer_name',customer_name.value) 
      });
      
      address.addEventListener('input',(e)=>{
        sessionStorage.setItem('address',address.value) 
      });
      
      
    }
  
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
    
    const shippingNameInput = document.getElementById("shipping_name");
    const shippingAddressTextarea = document.getElementById("shipping_address");
    const shippingStateSelect = document.getElementById("shipping_state");
    const shipping_state_trxn = document.getElementById("shipping_state_trxn");
    
    // tax_button.value = item.selectedOptions[0].getAttribute('tax'); {% endcomment %}
    // current_stock_button.value = item.selectedOptions[0].getAttribute('current_stock'); {% endcomment %}
    //  item.onclick = (e)=>{
    //   tax_button.value = item.selectedOptions[0].getAttribute('tax');
    //   current_stock_button.value = item.selectedOptions[0].getAttribute('current_stock');
    
    // };
  
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

    function same_state_check(shippingStateSelect)
    {
      if (shippingStateSelect.value==26)
          {
            // set display none of diff_state element
            for(let i of document.getElementsByClassName("diff_state"))
              {
                i.style.display="none";
              }
            for(let i of document.getElementsByClassName("same_state"))
              {
                i.style.display="block";
              }
          }
          else
          {
            for(let i of document.getElementsByClassName("same_state"))
              {
                i.style.display="none";
              }
            for(let i of document.getElementsByClassName("diff_state"))
              {
                i.style.display="block";
              }
          }
                          
    }
    if(shippingStateSelect)
      same_state_check(shippingStateSelect);

    function add_shipping_fields()
    {
        // add name_field
        name_code = '<div class="form-group"> <label>Customer name</label> <input required type="text" class="form-control remove_from_random_customer" name="customer_name" id="" value=""/></div>'
        node.innerHTML += name_code
        
        // add address_field
        address_code = '<div class="form-group"> <label>Address</label> <textarea class="form-control remove_from_random_customer" name="address" rows="10"></textarea></div>'
        node.innerHTML += address_code
        
        // add state field
        state_select_code = '<div class="form-group"> <label>State</label><select class="form-control" name="state"><option value="1">Andaman &amp; Nicobar Islands</option><option value="2">Andhra Pradesh</option><option value="3">Arunachal Pradesh</option><option value="4">Assam</option><option value="5">Bihar</option><option value="6">Chandigarh</option><option value="7">Chhattisgarh</option><option value="8">Dadra &amp; Nagar Haveli and Daman &amp; Diu</option><option value="9">Delhi</option><option value="10">Goa</option><option value="11">Gujarat</option><option value="12">Haryana</option><option value="13">Himachal Pradesh</option><option value="14">Jammu &amp; Kashmir</option><option value="15">Jharkhand</option><option value="16">Karnataka</option><option value="17">Kerala</option><option value="18">Ladakh</option><option value="19">Lakshadweep</option><option value="20">Madhya Pradesh</option><option value="21">Maharashtra</option><option value="22">Manipur</option><option value="23">Meghalaya</option><option value="24">Mizoram</option><option value="25">Nagaland</option><option value="26" selected="">Odisha</option><option value="27">Puducherry</option><option value="28">Punjab</option><option value="29">Rajasthan</option><option value="30">Sikkim</option><option value="31">Tamil Nadu</option><option value="32">Telangana</option><option value="33">Tripura</option><option value="34">Uttarakhand</option><option value="35">Uttar Pradesh</option><option value="36">West Bengal</option></select></div>'
        node.innerHTML += state_select_code

        node.classList.add("col-12")
        node.classList.add("col-sm-6")
    }
    
    let customer_selected = null
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
              add_shipping_fields()
              update_input_cash()
            }
          else
          {
            customer_selected = true;
          }
        },
        error: function(xhr, status, error) {
          // Handle the error if needed
          console.error(error);
        }
      });
    }
  
  
    function fetchIfCashAtStart(customerId) {
      $.ajax({
        url: '/finance/get_ifcash/',
        method: 'GET',
        data: { customerId: customerId },
        success: function(response) {
          node = document.querySelector(".random_customer");
          if(response.customer_is_cash == 1)
          {
              add_shipping_fields()
              update_input_cash()
            }
          else
          {

            // Create the checkbox and label elements
            const checkboxLabel = document.createElement("label");
            checkboxLabel.textContent = "Enter Shipping Address ";
            checkboxLabel.style.userSelect = "none"
            checkboxLabel.style.cursor = "pointer"

            checkboxLabel.style.color = "green"
            const shippingCheckbox = document.createElement("input");
            shippingCheckbox.type = "checkbox";
            shippingCheckbox.id = "shippingCheckbox";

            // Append the checkbox to the label and the label to the "shipping" div
            checkboxLabel.appendChild(shippingCheckbox);
            x = sessionStorage.getItem("shippingCheckbox")
            if(x)
              shippingCheckbox.checked=x;

            
            node.appendChild(checkboxLabel);
            const shippingAddressFields = document.createElement("div");

            node.classList.add("col-12")
            node.classList.add("col-sm-6")


            shippingCheckbox.addEventListener("change", function () {
                sessionStorage.setItem("shippingCheckbox", shippingCheckbox.checked)
                if (shippingCheckbox.checked) {
                    // Create and append the input fields when the checkbox is checked
                    shippingAddressFields.innerHTML = `
                    <div class="form-group"> <label>Name</label> <input type="text" class="form-control " name="shipping_name" id="shipping_name" value=""></div><div class="form-group"> <label>Address</label> <textarea class="form-control" name="shipping_address" id="shipping_address" rows="10"></textarea></div><div class="form-group"> <label>State</label><select class="form-control" name="shipping_state" id="shipping_state" ><option value="1">Andaman &amp; Nicobar Islands</option><option value="2">Andhra Pradesh</option><option value="3">Arunachal Pradesh</option><option value="4">Assam</option><option value="5">Bihar</option><option value="6">Chandigarh</option><option value="7">Chhattisgarh</option><option value="8">Dadra &amp; Nagar Haveli and Daman &amp; Diu</option><option value="9">Delhi</option><option value="10">Goa</option><option value="11">Gujarat</option><option value="12">Haryana</option><option value="13">Himachal Pradesh</option><option value="14">Jammu &amp; Kashmir</option><option value="15">Jharkhand</option><option value="16">Karnataka</option><option value="17">Kerala</option><option value="18">Ladakh</option><option value="19">Lakshadweep</option><option value="20">Madhya Pradesh</option><option value="21">Maharashtra</option><option value="22">Manipur</option><option value="23">Meghalaya</option><option value="24">Mizoram</option><option value="25">Nagaland</option><option value="26" selected="">Odisha</option><option value="27">Puducherry</option><option value="28">Punjab</option><option value="29">Rajasthan</option><option value="30">Sikkim</option><option value="31">Tamil Nadu</option><option value="32">Telangana</option><option value="33">Tripura</option><option value="34">Uttarakhand</option><option value="35">Uttar Pradesh</option><option value="36">West Bengal</option></select></div>
                    `;

                    // Set event listeners for the input fields to store their values in sessionStorage
                    const shippingNameInput = document.getElementById("shipping_name");
                    const shippingAddressTextarea = document.getElementById("shipping_address");
                    const shippingStateSelect = document.getElementById("shipping_state");
                    const shipping_state_trxn = document.getElementById("shipping_state_trxn");
                    x = sessionStorage.getItem("shipping_name")
                    if(x)
                      shippingNameInput.value=x;
                    shippingNameInput.addEventListener("input", function () {
                        sessionStorage.setItem("shipping_name", shippingNameInput.value);
                    });
                    x = sessionStorage.getItem("shipping_address")
                    if(x)
                    shippingAddressTextarea.value=x;
                    shippingAddressTextarea.addEventListener("input", function () {
                        sessionStorage.setItem("shipping_address", shippingAddressTextarea.value);
                    });
                    x = sessionStorage.getItem("shipping_state")
                    if(x)
                    shippingStateSelect.value=x;
                    shippingStateSelect.addEventListener("change", function () {
                        sessionStorage.setItem("shipping_state", shippingStateSelect.value);
                        shipping_state_trxn.value = shippingStateSelect.value
                        same_state_check(shippingStateSelect)
                        
                        // document.location.reload();
                    });
                } else {
                    // Remove the input fields when the checkbox is unchecked
                    shippingAddressFields.innerHTML = "";
                }
            });

            // Append the shippingAddressFields div to the "shipping" div
            node.appendChild(shippingAddressFields);
            
            
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
            },

      });
      $('#items_select2').selectize({
      onChange: function(value) {
        // Make an AJAX request to fetch the available quantity
        fetchAvailableQuantity2(value);
    }
});
$('#items_select2')[0].selectize.setValue("2")

$(function () {
    $("#customers_select").selectize({
        onChange: function(value) {
            // Make an AJAX request to fetch the if customer is cash and also assigns customer value to current_invoice
            if(value)
            {
              fetchIfCash(value);
              sessionStorage.setItem('cust_sel',value) 
              customer_id_in_transaction.value = value
              customer_id_in_transaction2.value = value
            }
            else
              console.error("The value is :" + value + "-" + typeof(value) + " - But it should be integer");          
            },
        });
      });
        
   });
  
  
  
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
    if(edit_transaction_button)
        edit_transaction_button.addEventListener("click",(e)=>{
        e.preventDefault();
        fetchTransactionDetails();
        });
  
    $(document).ajaxStop(function () {
      if (newRateValue !== null) {
        $('#rate2').val(newRateValue);
        newRateValue = null; // Reset newRateValue after updating rate2
      }
      if(customer_selected !== null)
      {
        customer_selected = null;
        document.location.reload() 
      }
    });
  
    
    

    
    document.addEventListener('DOMContentLoaded', function() {
        fetchIfCashAtStart($("#customers_select")[0].selectize.getValue());
        // document.querySelector("body").style.color = rgba(255,255,255,0.7)
        
    });
