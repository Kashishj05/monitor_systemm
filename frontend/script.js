const API_BASE = "http://localhost:8001";
let token = localStorage.getItem("token");
let currentUser = JSON.parse(localStorage.getItem("user"));

if (token && currentUser) {
  document.getElementById("login-section").style.display = "none";
  document.getElementById("task-section").style.display = "block";
  fetchTasks();
  if (currentUser.role === "admin" || currentUser.role === "manager") {
    loadUsers();
  }
}

async function register() {
  const username = document.getElementById("reg-username").value;
  const password = document.getElementById("reg-password").value;
  const role = document.getElementById("reg-role").value;

  try {
    const response = await fetch(`${API_BASE}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: username,
        name: username,
        password: password,
        role: role,
      }),
    });
    const data = await response.json();
    if (response.ok) {
      alert("Registration successful!");
    } else {
      alert("Registration failed: " + data.detail);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred during registration");
  }
}

async function login() {
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  try {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: username,
        password: password,
      }),
    });
    const data = await response.json();
    if (response.ok) {
      token = data.access_token;
      currentUser = data.user;
      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(currentUser));
      document.getElementById("login-section").style.display = "none";
      document.getElementById("task-section").style.display = "block";
      fetchTasks();
      if (currentUser.role === "admin" || currentUser.role === "manager") {
        loadUsers();
        fetchAllTasks();
        fetchAllTasks();
      }
    } else {
      alert("Login failed: " + data.detail);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred during login");
  }
}

async function createTask() {
  const title = document.getElementById("task-title").value;
  const description = document.getElementById("task-desc").value;
  const status = document.getElementById("task-status").value;
  const priority = document.getElementById("task-priority").value;
  const assigneeSelect = document.getElementById("task-assignee-select");
  const assigneeInput = document.getElementById("task-assignee");
  const assignee =
    assigneeSelect.style.display !== "none"
      ? assigneeSelect.value
      : assigneeInput.value;

  try {
    const response = await fetch(`${API_BASE}/tasks`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        title: title,
        description: description,
        priority: priority,
        assigned_to_email: assignee,
      }),
    });
    const data = await response.json();
    if (response.ok) {
      alert("Task created successfully!");
      fetchTasks();
      if (
        currentUser &&
        (currentUser.role === "admin" || currentUser.role === "manager")
      ) {
        fetchAllTasks();
      }
    } else {
      alert("Failed to create task: " + data.detail);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred while creating the task");
  }
}

async function loadUsers() {
  try {
    const response = await fetch(`${API_BASE}/auth/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const users = await response.json();
    if (response.ok) {
      const assigneeSelect = document.getElementById("task-assignee-select");
      assigneeSelect.innerHTML = '<option value="">Select Assignee</option>';
      users.forEach((user) => {
        const option = document.createElement("option");
        option.value = user.email;
        option.textContent = `${user.name} (${user.email})`;
        assigneeSelect.appendChild(option);
      });
      assigneeSelect.style.display = "block";
      document.getElementById("assignee-label").style.display = "block";
      document.getElementById("task-assignee").style.display = "none";
    } else {
      // Fallback to text input
      document.getElementById("task-assignee").style.display = "block";
      document.getElementById("assignee-label").style.display = "block";
      document.getElementById("assignee-label").textContent = "Assignee Email:";
      console.error("Failed to load users:", users.detail);
    }
  } catch (error) {
    // Fallback
    document.getElementById("task-assignee").style.display = "block";
    document.getElementById("assignee-label").style.display = "block";
    document.getElementById("assignee-label").textContent = "Assignee Email:";
    console.error("Error loading users:", error);
  }
}
try {
  const response = await fetch(`${API_BASE}/tasks/my`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  const tasks = await response.json();
  if (response.ok) {
    const list = document.getElementById("task-list");
    list.innerHTML = "";
    tasks.forEach((task) => {
      const li = document.createElement("li");
      li.textContent = `${task.title}: ${task.description} (Priority: ${task.priority})`;
      list.appendChild(li);
    });
  } else {
    alert("Failed to fetch tasks: " + tasks.detail);
  }
} catch (error) {
  console.error("Error:", error);
  alert("An error occurred while fetching tasks");
}

async function logout() {
  token = null;
  currentUser = null;
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  document.getElementById("task-section").style.display = "none";
  document.getElementById("login-section").style.display = "block";
  document.getElementById("register-section").style.display = "block";
}
try {
  const response = await fetch(`${API_BASE}/tasks/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  const tasks = await response.json();
  if (response.ok) {
    const list = document.getElementById("all-task-list");
    list.innerHTML = "";
    tasks.forEach((task) => {
      const li = document.createElement("li");
      li.textContent = `${task.title}: ${task.description} (Priority: ${task.priority}, Status: ${task.status})`;
      list.appendChild(li);
    });
  } else {
    console.error("Failed to fetch all tasks:", tasks.detail);
  }
} catch (error) {
  console.error("Error fetching all tasks:", error);
}
