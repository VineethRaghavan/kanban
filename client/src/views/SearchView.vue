<template>
    <div class="vue-template vh-100 d-flex align-items-center" v-on:submit.prevent="onSubmit">
        <div class="card mx-auto d-flex" style="width: 50rem; height: 40rem">
            <h3 class="card-header">Search</h3>
            <form class="form">
                <div class="form-group m-2 d-flex align-items-center">
                    <input v-model="text" type="text" @input="handleInput" placeholder="Search input" class="form-control form-control-lg m-2" />
                </div>
            </form>
            <div class="card-body overflow-auto" style="height: 15rem">
                <p> Number of records = {{ this.count }}</p>
                <table class="table">
                    <thead>
                        <tr>
                            <th scope="col">First name</th>
                            <th scope="col">Last name</th>
                            <th scope="col">Email</th>
                            <th scope="col">Birth date</th>
                            <th scope="col">Gender</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="emp in employees" :key="emp.emp_id" v-show="emp.found"> 
                            <td>{{ emp.fname }}</td>
                            <td>{{ emp.lname }}</td>
                            <td>{{ emp.email }}</td>
                            <td>{{ emp.birth_date }}</td>
                            <td>{{ emp.gender }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    name:"ChatView",
    data(){
        return{
            text: '',
            employees:null,
            count: 0
        }
    },
    computed:{
        isComplete(){
            return this.text != ''
        }
    },
    async created(){
        this.fetchData()
    },
    methods:{
        handleInput(event){
            let text = event.target.value
            let count = 0
            for(let emp of this.employees){
                if (emp.fname.toLowerCase().startsWith(text.toLowerCase()) || emp.lname.toLowerCase().startsWith(text.toLowerCase()) || emp.email.toLowerCase().startsWith(text.toLowerCase()) || emp.birth_date.toLowerCase().startsWith(text.toLowerCase())|| emp.gender.toLowerCase().startsWith(text.toLowerCase())){
                    emp.found = true
                    count += 1
                } else {
                    emp.found = false
                }
            }
            this.count = count
        },
        async fetchData(){
            let token = sessionStorage.getItem("accessToken");
            let request = {
                url: "http://localhost:5000/search",
                params:{ project_id: this.$route.query.project },
                method: "get",
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    "Content-type": "application/json",
                    'Authorization': `Bearer ${token}`
                },
            };
            try {
                const response = await axios(request);
                console.log(response);
                this.employees = response.data;
                this.count = response.data.length;
            } catch (error) {
                console.log(error)
                this.$router.push("/login");
            }
        },
    }
}
</script>