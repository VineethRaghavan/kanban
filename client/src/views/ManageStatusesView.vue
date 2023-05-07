<template>
    <div class="vue-template vh-100 d-flex" v-on:submit.prevent="onSubmit">
        <div class="card mx-auto d-flex m-5" style="min-height: 30rem">
            <h3 class="card-header">Manage statuses</h3>
            <form class="form">
                <div class="form-group m-2">
                    <input v-model="name" placeholder="Enter status name" type="text" class="form-control form-control-lg" />
                </div>
                <div class="form-group text-center">
                    <button :disabled="!isComplete" type="submit" class="btn btn-success btn-lg btn-block m-2">Add status</button>
                </div>
            </form>
            <div class="card mx-auto m-1">
                <h5 class="card-title text-center card-header">Statuses</h5>
                <div class="card-body overflow-auto" style="height: 16rem; width: 16rem">
                    <ul class="list-group list-group-flush ">
                        <li class="list-group-item" v-for="status in statuses" :key="status.status_id">
                            <div class="mx-auto d-flex justify-content-between align-items-center">
                                {{ status.name }}
                                <button type="button" class="close btn" aria-label="Close" @click="deleteStatus(status.status_id)">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    name:"manageStatusesView",
    data(){
        return{
            name: '',
            statuses: null
        }
    },
    computed:{
        isComplete(){
            return this.name.length != 0;
        }
    },
    async created(){
        this.fetchData()
    },
    methods:{
        async onSubmit(){
            let token = sessionStorage.getItem("accessToken")
            let data = {
                name: this.name
            };
            this.name = ""

            let request = {
                url: "http://localhost:5000/add_status",
                method: "post",
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    "Content-type": "application/json",
                    'Authorization': `Bearer ${token}`
                },
                data: JSON.stringify(data)
            };
            try {
                const response = await axios(request);
                console.log(response);
                this.fetchData();
                alert("Status added successfully");
            } catch (error) {
                console.log(error)
                alert(error.response.data.message)
            }
        },
        async deleteStatus(status_id){
            if(confirm("Are you sure you want to delete this status?")){
                let token = sessionStorage.getItem("accessToken")
                let data = {
                    status_id: status_id
                };

                let request = {
                    url: "http://localhost:5000/delete_status",
                    method: "post",
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        "Content-type": "application/json",
                        'Authorization': `Bearer ${token}`
                    },
                    data: JSON.stringify(data)
                };
                try {
                    const response = await axios(request);
                    console.log(response);
                    this.fetchData();
                    alert("Status deleted successfully");
                } catch (error) {
                    console.log(error)
                    alert(error.response.data.message)
                }
            }
        },
        async fetchData(){
            let token = sessionStorage.getItem("accessToken");
            let request = {
                url: "http://localhost:5000/statuses",
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
                this.statuses = response.data;
            } catch (error) {
                console.log(error)
                this.$router.push("/login");
            }
        }
    }
}
</script>