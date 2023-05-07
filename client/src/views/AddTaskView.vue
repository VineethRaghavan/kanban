<template>
    <div class="vue-template vh-100 d-flex align-items-center" v-on:submit.prevent="onSubmit">
        <div class="card mx-auto d-flex" style="width: 18rem;">
            <h3 class="card-header">Add task</h3>
            <form class="form">
                <div class="form-group m-2">
                    <label>Task name</label>
                    <input v-model="name" type="text" placeholder="Enter task name" class="form-control form-control-lg" />
                </div>
                <div class="form-group m-2">
                    <label>Status</label>
                    <select v-model="status" class="form-select" id="inputGroupSelect01">
                        <option :value="status.status_id" v-for="status in statuses" :key="status.status_id">{{ status.name }}</option>
                    </select>
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
                    <button :disabled="!isComplete" type="submit" class="btn btn-success btn-lg btn-block m-2">Add task</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    name:"AddTaskView",
    data(){
        return{
            name: '',
            status:'',
            statuses:null,
            project:this.$route.query.project,
            start_date: '',
            end_date: ''
        }
    },
    async created(){
        this.fetchData()
    },
    computed:{
        isComplete(){
            return this.name && this.start_date && this.end_date && this.status
        }
    },
    methods:{
        async onSubmit(){
            let token = sessionStorage.getItem("accessToken")
            let data = {
                name: this.name,
                status: this.status,
                project: this.project,
                start_date: this.start_date,
                end_date: this.end_date 
            };

            let request = {
                url: "http://localhost:5000/add_task",
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
                alert("Task added successfully")
                this.$router.push({path: "/tasks", query: { project: this.$route.query.project }})
            } catch (error) {
                console.log(error)
                alert(error.response.data.message)
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