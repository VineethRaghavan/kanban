import { createWebHistory, createRouter } from "vue-router";
import Login from "@/views/LoginView.vue";
import Register from "@/views/RegisterView.vue";
import Projects from "@/views/ProjectsView.vue";
import AddProject from "@/views/AddProjectView.vue";
import Tasks from "@/views/TasksView.vue";
import ManageStatuses from "@/views/ManageStatusesView.vue";
import AddTask from '@/views/AddTaskView.vue';
import EditProfile from '@/views/EditProfileView.vue';
import Chat from '@/views/ChatView.vue';
import Search from '@/views/SearchView.vue';
import Landing from '@/views/LandingView.vue';

const routes = [
    {
        path:"/",
        name:"Landing",
        component: Landing
    },
    {
        path:"/login",
        name:"Login",
        component: Login
    },
    {
        path:"/edit_profile",
        name:"EditProfile",
        component: EditProfile
    },
    {
        path:"/register",
        name:"Register",
        component: Register
    },
    {
        path:"/projects",
        name:"Projects",
        component: Projects
    },
    {
        path:"/add_project",
        name:"AddProject",
        component: AddProject
    },
    {
        path:"/tasks",
        name:"Tasks",
        component: Tasks
    },
    {
        path:"/manage_statuses",
        name:"ManageStatuses",
        component: ManageStatuses
    },
    {
        path:"/add_task",
        name:"AddTask",
        component: AddTask
    },
    {
        path:"/chat",
        name:"Chat",
        component: Chat
    },
    {
        path:"/search",
        name:"Search",
        component: Search
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;