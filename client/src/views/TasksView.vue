<template>
    <div class="mx-auto d-flex justify-content-between border-bottom">
        <h3 class="m-3">Tasks</h3>
        <button type="button" @click="addTask" class="btn btn-success btn-block m-3">Add new task</button>
        <button type="button" @click="onCommit" class="btn btn-primary btn-block m-3">Save</button>
        <button type="button" @click="openChat" class="btn btn-warning btn-block m-3">Chat</button>
        <button type="button" @click="logOut" class="btn btn-outline-secondary btn-block m-3">Log out</button>
    </div>
    <div class="vue-template vh-75 d-flex flex-wrap justify-content-center">
        <div v-for="[status_id, tasks] in Object.entries(tasks_list)" :key="status_id" class="card row m-3 d-flex flex-wrap text-center">
            <h3 class="card-title text-center card-header">{{ status_list.get(status_id) }} - {{ tasks.length }} </h3>
            <div class="col">
                <draggable
                    class="list-group"
                    :list="tasks"
                    group="tasks"
                    itemKey="id"
                >
                    <template #item="{ element }">
                        <div class="card m-2">
                            <h5 class="card-title text-center card-header">{{ element.name }}</h5>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item">Start date: {{ element.start_date }}</li>
                                <li class="list-group-item">End date: {{ element.end_date }}</li>
                                <li class="list-group-item">Employee: {{ element.employee }}</li>
                            </ul>
                            <button type="button" @click="deleteTask(element.task_id)" class="btn btn-danger btn-block m-3">Delete</button>
                        </div>
                    </template>
                </draggable>
            </div>
        </div>
    </div>
</template>

<script>
import draggable from 'vuedraggable'
import axios from 'axios'

export default{
    name:"TasksView",
    components: {
        draggable
    },
    data() {
        return {
            tasks_list:{},
            status_list:null,
        }
    },
    async created(){
        this.fetchData();
    },
    methods:{
        logOut(){
            sessionStorage.clear();
            this.$router.push("/login");
        },
        addTask(){
            this.$router.push({path: "/add_task", query: { project: this.$route.query.project }})
        },
        openChat(){
            this.$router.push({path: "/chat", query: { project: this.$route.query.project }})
        },
        onCommit: async function(){
            console.log(JSON.parse(JSON.stringify(this.tasks_list)))
            let token = sessionStorage.getItem("accessToken")
            let data = this.tasks_list
            console.log(this.$route.query.project.toString())

            let request = {
                url: "http://localhost:5000/save_tasks",
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
                alert("Tasks saved successfully")
                this.$router.push({path: "/tasks", query: { project: this.$route.query.project }})
            } catch (error) {
                console.log(error)
                alert(error.response.data.message)
            }
        },
        async deleteTask(task_id){
            if(confirm("Are you sure you want to delete this task?")){
                let token = sessionStorage.getItem("accessToken")
                let data = {
                    task_id: task_id,
                    project_id: this.$route.query.project
                };

                let request = {
                    url: "http://localhost:5000/delete_task",
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
                    alert("Task deleted successfully");
                } catch (error) {
                    console.log(error)
                    alert(error.response.data.message)
                }
            }
        },
        async fetchData(){
            let token = sessionStorage.getItem("accessToken");
            this.$route.query.project.toString()
            let request = {
                url: "http://localhost:5000/tasks",
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
                this.tasks_list = response.data.tasks;
                this.status_list = new Map(Object.entries(response.data.status));
            } catch (error) {
                console.log(error)
                this.$router.push("/login");
            }
        }
    }
}
</script>