
function round(number,digits=2){
  var decimal = number * Math.pow(10,digits)
  decimal = Math.round(decimal) / 100
  return(decimal)
}

const invoice_no_input = document.getElementById("invoice_no")
const date_input = document.getElementById("date")
const cust_sel = document.querySelector("#customers_select")
const item_selector = document.querySelector("#items_select")
const item_selector2 = document.querySelector("#items_select2")
const separator = "$$$"
const divide_separator = "$$$&&^^@#"
const table = document.querySelector("#myTable tbody")
const add_button = document.querySelector("#addItem .submit")
const update_button = document.querySelector("#editTransaction .submit")
const save_invoice_button = document.querySelector('#saveInvoice')
const extra_detail = document.querySelector("#myTable tfoot")
const add_item_button = document.getElementById("add_item")
var edit_transaction_buttons = document.querySelectorAll(".edit_transaction_button")

// function to get transactions
function get_trxn_from_storage(string_value)
{
  var trxn = string_value.split(divide_separator)
  trxn.forEach((elem,index)=>{
    trxn[index] = elem.split(separator);
  });
  return trxn;
}

function get_trxn_addon_from_storage(string_value)
{
  var trxn = string_value.split(divide_separator)
  trxn.forEach((elem,index)=>{
    trxn[index] = elem.split(separator);
  });
  return trxn;
}

function update_trxn_addon_session_storage()
{
  obj = []
  for(j=2;j<extra_detail.children.length-5;j++)
    {
        let name = extra_detail.children[j].querySelector("input[type='text']").value
        let value = extra_detail.children[j].querySelector("input[type='number']").value
        s = name+separator+value
        obj.push(s)
    }
  localStorage.setItem("transaction_addon",obj.join(divide_separator))
}
function update_trxn_session_storage()
{
  z = table.children 
  obj = []
  for(let i=0;i<z.length;i++){
    s = []
    for(let j=0;j<6;j++){
        // console.log(z[i])
        s.push(z[i].children[j].textContent)
    }
    obj.push(s.join(separator))
  }
  obj = obj.join(divide_separator)
  localStorage.setItem("transaction",obj)
}

function get_edit_delete_btn()
{
  // exclusively only for transaction part
  //NOTE: dont even use it in transaction addons
  z = document.createElement("td")
  z.classList.add("text-end")

  // for edit button
  btn = document.createElement("button")
  btn.classList.add("btn","btn-primary","btn-sm","edit_row","m-2")
  btn.setAttribute("data-toggle","modal")
  btn.setAttribute("data-target","#editTransaction")
  btn.textContent = "Edit"
  z.appendChild(btn)
  // to open modal #modal-form2
  btn.onclick = (e)=>{
    e.preventDefault();
    
    // remove all .edit row from the table 
    document.querySelectorAll(".edit_row").forEach((row)=>{
      row.classList.remove("edit_row")
    })
    
    // add to its row class list .edit_row 
    row = e.target.parentElement.parentElement
    row.classList.add("edit_row")

    // update the values of the modal form
    item_selector2.selectize.setValue(item_selector2.selectize.search(row.children[0].textContent).items[0].id)
    tax_button2.value = row.children[1].textContent
    qnt2.value = row.children[2].textContent
    rate2.value = row.children[3].textContent
    discount_percent2.value = row.children[4].textContent
    discount_amount2.value = round( taxable_value2.value * discount_percent2.value / 100,2);
    taxable_value2.value = row.children[5].textContent
    total_amount2.value = round( ((taxable_value2.value-discount_amount2.value) * (1 + (tax_button2.value*2)/100)),2);
    total_rate2.value = round( total_amount2.value / qnt2.value,2);
  }
  btn = document.createElement("button")
  btn.classList.add("btn","btn-danger","btn-sm","delete_row")
  btn.textContent = "Delete"
  btn.onclick = (e)=>{
    e.preventDefault();
    row = e.target.parentElement.parentElement
    row.remove()
    update_totals()
  }
  z.appendChild(btn)
  return z;
}

// localStorage.setItem('cust_sel','Select Customer') 

function update_random_customer(case_no)
{
  // 3 cases in total

  // 1. Customer is cash 
  // 2. Customer has to enter shipping address 
  // 3 (else). Customer doesnt need any of that

  // checkbox = document.querySelector(".change_shipping_address") 
  customer_name = document.getElementById("shipping_customer_name")
  address = document.getElementById("shipping_address")
  state = document.getElementById("shipping_state")
  if(case_no == 1)
  {
    console.log("Case 1 executed")
    node.style.display="block"
    
    data = localStorage.getItem('customer_name') 
    if(data)
      customer_name.value = data;  
    
    data = localStorage.getItem('address') 
    if(data)
      address.value = data;
    
    data = localStorage.getItem('state') 
    if(data)
      state.value = data
      

    customer_name.addEventListener('input',(e)=>{
      localStorage.setItem('customer_name',customer_name.value) 
    });
    
    address.addEventListener('input',(e)=>{
      localStorage.setItem('address',address.value) 
    });
    
    state.addEventListener('change',(e)=>{
      localStorage.setItem('state',state.value);
    });

    // add the required role here
    customer_name.setAttribute("required",true) 
    address.setAttribute("required",true) 

  }
  else if(case_no == 2)
  {
    console.log("Case 2 executed")
    node.style.display="block" 
    
    data = localStorage.getItem('customer_name') 
    if(data)
      customer_name.value = data;  
    
    data = localStorage.getItem('address') 
    if(data)
      address.value = data;
    
    data = localStorage.getItem('state') 
    if(data)
      state.value = data;
      

    customer_name.addEventListener('input',(e)=>{
      localStorage.setItem('customer_name',customer_name.value) 
    });
    
    address.addEventListener('input',(e)=>{
      localStorage.setItem('address',address.value) 
    });
    
    state.addEventListener('change',(e)=>{
      localStorage.setItem('state',state.value) 
    });

    customer_name.setAttribute("required",true) 
    address.setAttribute("required",true) 
  }
  else
  {
    node.style.display = "none"
    checkbox.style.display = "block"

    customer_name.removeAttribute("required") 
    address.removeAttribute("required")

    customer_name.removeEventListener('input',(e)=>{
      localStorage.setItem('customer_name',customer_name.value) 
    });
    
    address.removeEventListener('input',(e)=>{
      localStorage.setItem('address',address.value) 
    });
    
    state.removeEventListener('change',(e)=>{
      localStorage.setItem('state',state.value) 
    });
  }
} // closed update input random customer

const checkbox = document.getElementById("change_shipping_address")
checkbox.addEventListener("change",(e)=>{
  if(e.target.checked)
  {
    update_random_customer(2)
  }
  else 
  {
    update_random_customer(3)
  }
  localStorage.setItem("checked_shipping",e.target.checked)
})



data = localStorage.getItem('invoice_no') 
if(data)
  invoice_no_input.value = data;

data = localStorage.getItem('cust_sel') 
if(data)
{
  cust_sel.value = data;
  customer_id_in_transaction.value = data
  customer_id_in_transaction2.value = data
}
data = localStorage.getItem('date') 
if(data)
  date_input.value = data;

data = localStorage.getItem('transaction')
if(data)
{
  trxn = get_trxn_from_storage(data)
  table.innerHTML = ""
  trxn.forEach((elem,index)=>{
    row = table.insertRow(-1);
    row.innerHTML = `
    <td>${elem[1]}</td>
    <td>${elem[2]}</td>
    <td>${elem[3]}</td>
    <td>${elem[4]}</td>
    <td>${elem[5]}</td>
    <td>${elem[6]}</td>
    `;
    z = get_edit_delete_btn()
    row.appendChild(z);
    invoice_taxable_value += parseFloat(taxable_value.value)
    invoice_total_amount += parseFloat(total_amount.value)
  })
}
data = localStorage.getItem('transaction_addon')

if(data)
{
  trxn = get_trxn_addon_from_storage(data)
  // index = 2
  trxn.forEach((elem,index)=>{
    row = extra_detail.insertRow(index+2);
    console.log(elem)
    row.innerHTML = `
    <td colspan="2"></td>
  <td class="text-end" colspan="2"><strong><input class="form-control" value="${elem[0]}" type="text"></strong></td>
  <td colspan="1"></td>
  <td><input class="form-control px-0" value="${elem[1]}" type="number" step="0.01" disabled ></td>
    `;

    // add one more td
    td = document.createElement("td")
    btn = document.createElement("button")
    btn.classList.add("btn","btn-danger","btn-sm","delete_row")
    btn.innerHTML = `<i class="fas fa-trash"></i>`
    btn.onclick = ()=>{
      row.remove();
    }
    td.appendChild(btn)
    row.appendChild(td);
    // invoice_taxable_value += parseFloat(taxable_value.value)
    invoice_total_amount += parseFloat(elem[1])
    })
  }



document.getElementById("reset").addEventListener("click",(e)=>{
  localStorage.clear()
  customer_id_in_transaction.value = "2"
  customer_id_in_transaction2.value = "2"
})

// session storage
invoice_no_input.addEventListener('input',(e)=>{
  localStorage.setItem('invoice_no',document.getElementById("invoice_no").value) 
});

date_input.addEventListener('input',(e)=>{
  localStorage.setItem('date',document.getElementById("date").value) 
});


const qnt = document.querySelector("#modal-form #qnt")
const qnt2 = document.querySelector("#modal-form2 #qnt2")

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
    console.log(taxable_value.value)
    rate.value = round( parseFloat(taxable_value.value) / qnt_no,2);
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


edit_transaction_buttons.forEach((button)=>{
  button.addEventListener("click",(e)=>{
    e.preventDefault();
    console.log(button);
});
});
console.log("Edit Transaction Buttons:",edit_transaction_buttons)

let newRateValue = null;
$(document).ready(function() {
  
  $('#items_select').selectize({
    onChange: function(value) {
      // Make an AJAX request to fetch the available quantity and tax percent for the selected item
      $.ajax({
        url: '/finance/get_tax_quantity/',
        data: {
          'item_id': value,
          "customer_id":customer_id_in_transaction.value
        },
        dataType: 'json',
        success: function (data) {
          // Update the #current_stock field,#rate field and #tax field
          $('#rate').val(data.rate);
          $('#tax').val(data.tax);
          $('#current_stock').val(data.available_quantity);
          $('#edit_item').attr('href',data.edit_item_url)
          // update the #qnt field
          qnt.setAttribute("max",data.available_quantity);
          qnt.value = 0;
        }
      });
      
    }
  });
  $('#items_select2').selectize({
  onChange: function(value) {
    // Make an AJAX request to fetch the available quantity and tax percent for the selected item
    $.ajax({
      url: '/finance/get_tax_quantity/',
      data: {
        'item_id': value,
        "customer_id":customer_id_in_transaction2.value
      },
      dataType: 'json',
      success: function (data) {
        // Update the #current_stock field,#rate field and #tax field
        $('#rate2').val(data.rate);
        $('#tax2').val(data.tax);
        $('#current_stock2').val(data.available_quantity);
        $('#edit_item2').attr('href',data.edit_item_url)

        // update the #qnt field
        qnt2.setAttribute("max",data.available_quantity);
        qnt2.value = 0;
      }
    });
    }
  });
});



$(document).ajaxStop(function () {
if (newRateValue !== null) {
  $('#rate2').val(newRateValue);
  newRateValue = null; // Reset newRateValue after updating #rate2
}
});



// table 
// updating th values on add button click

add_button.addEventListener("click",(e)=>{
  e.preventDefault();
  // add the table row fields(Item	Tax (in %)	Quantity	Rate	Discount (in %)	Taxable Value)
  row = table.insertRow(-1);
  var item_name = item_selector.selectize.getItem(item_selector.value)[0].textContent.split("\n")[1].trim();
  var id = table.children.length + 1
  row.innerHTML = `
  <td>${item_name}</td>
  <td>${tax_button.value}</td>
  <td>${qnt.value}</td>
  <td>${rate.value}</td>
  <td>${discount_percent.value}</td>
  <td>${taxable_value.value}</td>
  `;
  
  // save to storage 
  // js obj 
  
  obj = [
    id,
		item_name,
		tax_button.value,
		qnt.value,
		rate.value,
		discount_percent.value,
		taxable_value.value
  ]   // 7 rows
  
  
  // get the old string
  old_string = localStorage.getItem("transaction")
  if (!old_string)
  {
    localStorage.setItem("transaction",obj.join(separator))
  }
  else
  {
    obj = old_string + divide_separator + obj.join(separator)
    localStorage.setItem("transaction",obj)
  }
  
  
  z = get_edit_delete_btn();
  row.appendChild(z)
    
  invoice_taxable_value += parseFloat(taxable_value.value)
  invoice_total_amount += parseFloat(total_amount.value)
  update_totals();
});

update_button.addEventListener("click",(e)=>{
  e.preventDefault()
  // get the row for which it is called 
  row = document.querySelector(".edit_row")
  row.children[0].textContent = item_selector2.selectize.getItem(item_selector2.value)[0].textContent.split("\n")[1].trim()
  row.children[1].textContent = tax_button2.value
  row.children[2].textContent = qnt2.value
  row.children[3].textContent = rate2.value
  row.children[4].textContent = discount_percent2.value
  row.children[5].textContent = taxable_value2.value
  update_trxn_session_storage()

});

// add transaction button 
add_transaction_button = document.querySelector("#addTransaction .submit")
// my table footer 

name_input = document.querySelector('#addTransaction input[name="name_in_trxn"]')
amount_input = document.querySelector('#addTransaction input[name="amount_in_trxn"]')
add_transaction_button.addEventListener("click",(e)=>{
  
  e.preventDefault();
  // add two input fields //
  // 1. name  
  // 2. value
  // 3. delete button
  string = `<td colspan="2"></td>
  <td class="text-end" colspan="2"><strong><input class="form-control" value = "${name_input.value}" type="text" /></strong></td>
  <td colspan="1"></td>
  <td><input class="form-control" value = "${amount_input.value}" type="number" step="0.01" disabled /></td>
  `

  el = document.createElement("tr")
  el.innerHTML = string
  btn = document.createElement("button")
  btn.classList.add("btn","btn-danger","btn-sm","delete_row")
  btn.innerHTML = "<i class='fas fa-trash'></i>"

  btn.onclick = (e)=>{
    e.preventDefault();
    row = e.target.parentElement.parentElement
    while (row.tagName != "TR")
    {
      row = row.parentElement
    }
    row.remove()
    update_totals()
  }
  x = document.createElement("td")
  x.appendChild(btn)
  el.appendChild(x)

  obj = [
    name_input.value,
    amount_input.value
  ]

  old_string = localStorage.getItem("transaction_addon")
  if (!old_string)
  {
    localStorage.setItem("transaction_addon",obj.join(separator))
  }
  else
  {
    obj = old_string + divide_separator + obj.join(separator)
    localStorage.setItem("transaction_addon",obj)
  }
  

  // insert to second last position
  extra_detail.insertBefore(el,extra_detail.children[extra_detail.children.length-5])
  update_totals()
});


save_invoice_button.addEventListener("click",(e)=>{
  e.preventDefault();

  // Add the loading screen
  const pagewrapper = document.querySelector("body")
  pagewrapper.classList.add("loading")


  // get the form data
  invoice_no = invoice_no_input.value
  date = date_input.value
  customer_id = customer_id_in_transaction.value
  tax_type = document.querySelector("#tax_type").value

  // get the shipping address
  change_shipping_address = document.querySelector("#change_shipping_address").checked
  shipping_customer_name = document.querySelector("#shipping_customer_name").value
  state = document.querySelector("#shipping_state").value
  address = document.querySelector("#shipping_address").value

  // get the transaction data
  transaction = localStorage.getItem("transaction")
  // get the transaction addon data
  transaction_addon = localStorage.getItem("transaction_addon")

  // wrap them into json
  data = {
    "invoice_no":invoice_no,
    "date":date,
    "customer_id":customer_id,
    "tax_type":tax_type,
    "change_shipping_address":change_shipping_address,
    "customer_shipping":shipping_customer_name,
    "state":state,
    "address":address,
    "transaction":transaction,
    "transaction_addon":transaction_addon
  }
  

  // async save them
  $.ajax({
    type: "GET",
    url: "/finance/save_invoice/",
    data: data,
    dataType: "json",
    success: function (response) {
      if(response.status == "success")
      {
        window.location.href = "/finance/view_invoices/"
      }
      else
      {
        console.warn(response)
      }
      // remove the loading screen
      pagewrapper.classList.remove("loading")
    },
    error: function (response){
      console.log("Saad There is problem")
      alert("Error:"+response.statusText)
      // remove the loading screen
      pagewrapper.classList.remove("loading")
    }
  });
  // send data to "/finance/save_invoice/" async 


  // get the response
  // if success then redirect to the invoice page
  // else show the error message
});