<template>
    <div class="vue-template vh-100 d-flex align-items-center" v-on:submit.prevent="onSubmit">
        <div class="card mx-auto d-flex" style="width: 18rem;">
            <h3 class="card-header">Add project</h3>
            <form class="form">
                <div class="form-group m-2">
                    <label>Project name</label>
                    <input v-model="name" type="text" placeholder="Enter project name" class="form-control form-control-lg" />
                </div>
                <div class="form-group m-2">
                    <label>Start date</label>
                    <input v-model="start_date" type="date" class="form-control form-control-lg" />
                </div>
                <div class="form-group m-2">
                    <label>End date</label>
                    <input v-model="end_date" type="date" class="form-control form-control-lg" />
                </div>
                <div class="form-group text-center">
                    <button :disabled="!isComplete" type="submit" class="btn btn-success btn-lg btn-block m-2">Add project</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    name:"AddProjectView",
    data(){
        return{
            name: '',
            start_date: '',
            end_date: ''
        }
    },
    computed:{
        isComplete(){
            return this.name && this.start_date && this.end_date
        }
    },
    methods:{
        async onSubmit(){
            let token = sessionStorage.getItem("accessToken")
            let data = {
                name: this.name,
                start_date: this.start_date,
                end_date: this.end_date 
            };

            let request = {
                url: "http://localhost:5000/add_project",
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
                alert("Project added successfully")
                this.$router.push("/projects");
            } catch (error) {
                console.log(error)
                alert(error.response.data.message)
            }
        }
    }
}
</script>