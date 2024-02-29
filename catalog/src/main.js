import { createApp } from 'vue'

import PrimeVue from 'primevue/config';
import '/node_modules/primeflex/primeflex.css'
import 'primevue/resources/themes/lara-dark-purple/theme.css'
import 'primeicons/primeicons.css'

import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Row from 'primevue/row';                   // optional
import InputText from 'primevue/inputtext';                   // optional
import Tag from 'primevue/tag';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import Card from 'primevue/card';
import SelectButton from 'primevue/selectbutton';

import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';

import Catalog from './components/Catalog.vue';

import App from './App.vue'
const app = createApp(App);
app.use(PrimeVue);

app.component('DataTable', DataTable);
app.component('Column', Column);
app.component('Row', Row);
app.component('Button', Button);
app.component('InputText', InputText);
app.component('Dropdown', Dropdown);
app.component('Tag', Tag)
app.component('Card', Card)
app.component('SelectButton', SelectButton)

app.component('IconField', IconField)
app.component('InputIcon', InputIcon)

app.component('Catalog', Catalog)

app.mount('#app');