<template>
  <div id="checkaccountapp">

    <form @submit.prevent="createCheckAccount">
      <div class="form-group row">
        <input type="text" class="form-control col-3 mx-2" placeholder="Firma tipi" v-model="account.firm_type">
        <input type="text" class="form-control col-3 mx-2" placeholder="Firma ismi" v-model="account.firm_full_name">
        <input type="text" class="form-control col-3 mx-2" placeholder="Kimlik no" v-model="account.taxpayer_number">
        <input type="text" class="form-control col-3 mx-2" placeholder="Doğum yeri" v-model="account.birthplace">
        <input type="text" class="form-control col-3 mx-2" placeholder="Vergi Departmanı" v-model="account.tax_department">
        <input type="text" class="form-control col-3 mx-2" placeholder="Firma adresi" v-model="account.firm_address">
        <input type="text" class="form-control col-3 mx-2" placeholder="Firma iletişim personeli" v-model="account.firm_key_contact_personnel">
        <input type="text" class="form-control col-3 mx-2" placeholder="Sektör" v-model="account.sector">
        <input type="text" class="form-control col-3 mx-2" placeholder="Şehir" v-model="account.city">
        <input type="text" class="form-control col-3 mx-2" placeholder="İlçe" v-model="account.district">
        <input type="text" class="form-control col-3 mx-2" placeholder="Telefon" v-model="account.phone_number">
        <input type="text" class="form-control col-3 mx-2" placeholder="Fax" v-model="account.fax">
        <input type="text" class="form-control col-3 mx-2" placeholder="Web url" v-model="account.web_url">
        <input type="text" class="form-control col-3 mx-2" placeholder="E-mail" v-model="account.email_addr">

        <button class="btn btn-success"> Oluştur</button>
      </div>
    </form>

    <div class="container">
      <table class="table">
        <thead>
        <th> Firma tipi</th>
        <th> Firma ismi</th>
        <th> Kimlik no</th>
        <th> Doğum yeri</th>
        <th> Vergi Departmanı</th>
        <th> Firma adresi</th>
        <th> Firma iletişim personeli</th>
        <th> Sektör</th>
        <th> Şehir</th>
        <th> İlçe</th>
        <th> Telefon</th>
        <th> Fax</th>
        <th> Web url</th>
        <th> Email</th>
        </thead>

        <tbody>
        <tr v-for="account in accounts" :key="account.pk">
          <td>{{ account.firm_type }}</td>
          <td>{{ account.firm_full_name }}</td>
          <td>{{ account.taxpayer_number }}</td>
          <td>{{ account.birthplace }}</td>
          <td>{{ account.tax_department }}</td>
          <td>{{ account.firm_address }}</td>
          <td>{{ account.firm_key_contact_personnel }}</td>
          <td>{{ account.sector }}</td>
          <td>{{ account.city }}</td>
          <td>{{ account.district }}</td>
          <td>{{ account.phone_number }}</td>
          <td>{{ account.fax }}</td>
          <td>{{ account.web_url }}</td>
          <td>{{ account.email_addr }}</td>
        </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {
      account: {
        'firm_type' : '',
        'firm_full_namer' : '',
        'taxpayer_number' : '',
        'birthplace' : '',
        'tax_department' : '',
        'firm_address' : '',
        'firm_key_contact_personnel' : '',
        'sector' : '',
        'city' : '',
        'district' : '',
        'phone_number' : '',
        'fax' : '',
        'web_url' : '',
        'email_addr' : '',
      },

      accounts: []
    }
  },

  async created() {
    var response = await fetch('http://localhost:8000/checkaccount/api/accounts/')
    this.accounts = await response.json();

  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
