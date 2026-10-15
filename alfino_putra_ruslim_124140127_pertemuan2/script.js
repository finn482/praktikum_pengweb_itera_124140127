const TASKS_KEY = "studyflow-tasks-v1";
const QUOTE_API = "https://dummyjson.com/quotes/random";
const TODO_API = "https://jsonplaceholder.typicode.com/todos?_limit=5";

class TaskItem {
  constructor({ id = globalThis.crypto?.randomUUID?.() || `task-${Date.now()}-${Math.random().toString(16).slice(2)}`, title, course = "Umum", dueDate, priority = "medium", note = "", completed = false }) {
    this.id = id;
    this.title = title;
    this.course = course || "Umum";
    this.dueDate = dueDate;
    this.priority = priority;
    this.note = note;
    this.completed = completed;
  }

  toggle() {
    this.completed = !this.completed;
    return this;
  }

  toJSON() {
    return { ...this };
  }
}

class DashboardApp {
  constructor() {
    this.tasks = [];
    this.activeFilter = "all";
    this.searchTerm = "";
    this.editingId = null;
    this.quoteTimer = null;
    this.elements = this.getElements();
    this.bindEvents();
    this.initialize();
  }

  getElements() {
    const query = (selector) => document.querySelector(selector);
    return {
      taskList: query("#task-list"), emptyTasks: query("#empty-tasks"), dialog: query("#task-dialog"), form: query("#task-form"),
      dialogTitle: query("#dialog-title"), taskId: query("#task-id"), title: query("#task-title"), course: query("#task-course"), dueDate: query("#task-due"),
      priority: query("#task-priority"), note: query("#task-note"), titleError: query("#title-error"), dueError: query("#due-error"),
      search: query("#search-task"), currentDate: query("#current-date"), activeCount: query("#active-count"), doneCount: query("#done-count"), urgentCount: query("#urgent-count"),
      quote: query("#quote-text"), author: query("#quote-author"), toast: query("#toast")
    };
  }

  bindEvents() {
    const { form, taskList, search, dialog } = this.elements;
    document.querySelector("#add-task-button").addEventListener("click", () => this.openDialog());
    document.querySelector("#close-dialog").addEventListener("click", () => dialog.close());
    document.querySelector("#cancel-dialog").addEventListener("click", () => dialog.close());
    document.querySelector("#refresh-quote").addEventListener("click", () => this.loadQuote());
    document.querySelectorAll("[data-filter]").forEach((button) => button.addEventListener("click", ({ currentTarget }) => {
      this.activeFilter = currentTarget.dataset.filter;
      document.querySelectorAll("[data-filter]").forEach((tab) => tab.classList.toggle("active", tab === currentTarget));
      this.renderTasks();
    }));
    search.addEventListener("input", ({ target }) => { this.searchTerm = target.value.toLowerCase().trim(); this.renderTasks(); });
    form.addEventListener("submit", (event) => this.handleSubmit(event));
    taskList.addEventListener("click", (event) => this.handleTaskAction(event));
    taskList.addEventListener("change", ({ target }) => { if (target.matches(".task-check")) this.toggleTask(target.dataset.id); });
  }

  async initialize() {
    this.elements.currentDate.textContent = new Intl.DateTimeFormat("id-ID", { dateStyle: "full" }).format(new Date());
    this.tasks = this.loadTasks();
    if (this.tasks.length === 0) await this.seedTasks();
    this.renderAll();
    await this.loadQuote();
  }

  loadTasks() {
    try {
      const saved = localStorage.getItem(TASKS_KEY);
      const parsed = saved ? JSON.parse(saved) : [];
      return Array.isArray(parsed) ? parsed.map((task) => new TaskItem(task)) : [];
    } catch (error) {
      console.warn("Data tugas tidak dapat dibaca.", error);
      return [];
    }
  }

  saveTasks() {
    localStorage.setItem(TASKS_KEY, JSON.stringify(this.tasks.map((task) => task.toJSON())));
  }

  async seedTasks() {
    try {
      const response = await fetch(TODO_API);
      if (!response.ok) throw new Error("Gagal mengambil data tugas awal");
      const todos = await response.json();
      const today = new Date();
      this.tasks = todos.map(({ id, title, completed }, index) => new TaskItem({
        id: `seed-${id}`, title: title.charAt(0).toUpperCase() + title.slice(1), course: ["PAW", "Basis Data", "PBO", "Jaringan", "Kewirausahaan"][index],
        dueDate: this.toDateInput(new Date(today.getTime() + (index + 1) * 86400000)), priority: index < 2 ? "high" : "medium", completed
      }));
      this.saveTasks();
      this.showToast("Tugas contoh berhasil dimuat dari API.");
    } catch (error) {
      console.warn("Seed API tidak tersedia, dashboard dimulai kosong.", error);
      this.showToast("Mode offline aktif. Tambahkan tugas pertamamu.");
    }
  }

  async loadQuote() {
    this.elements.quote.textContent = "Mengambil inspirasi...";
    try {
      const response = await fetch(QUOTE_API);
      if (!response.ok) throw new Error("Kutipan tidak tersedia");
      const { quote, author } = await response.json();
      this.elements.quote.textContent = quote;
      this.elements.author.textContent = `— ${author}`;
    } catch (error) {
      this.elements.quote.textContent = "Konsistensi kecil setiap hari menghasilkan perubahan besar.";
      this.elements.author.textContent = "— StudyFlow";
    }
  }

  getVisibleTasks() {
    const matchesFilter = (task) => this.activeFilter === "all" || (this.activeFilter === "done" ? task.completed : !task.completed);
    const matchesSearch = (task) => `${task.title} ${task.course} ${task.note}`.toLowerCase().includes(this.searchTerm);
    return this.tasks.filter((task) => matchesFilter(task) && matchesSearch(task));
  }

  renderAll() {
    this.renderTasks();
    this.renderStats();
    this.renderAgenda();
  }

  renderTasks() {
    const visibleTasks = this.getVisibleTasks();
    this.elements.taskList.innerHTML = visibleTasks.map((task) => this.taskTemplate(task)).join("");
    this.elements.emptyTasks.hidden = visibleTasks.length > 0;
  }

  taskTemplate(task) {
    const { id, title, course, dueDate, priority, note, completed } = task;
    const due = this.formatDueDate(dueDate);
    return `<article class="task-item">
      <input class="task-check" type="checkbox" data-id="${this.escape(id)}" ${completed ? "checked" : ""} aria-label="Tandai ${this.escape(title)} sebagai ${completed ? "belum selesai" : "selesai"}">
      <div><span class="task-title ${completed ? "completed" : ""}">${this.escape(title)}</span><span class="task-meta">${this.escape(course)}${note ? ` · ${this.escape(note)}` : ""}</span></div>
      <span class="priority priority-${priority}">${this.priorityLabel(priority)}</span>
      <span class="due-label ${due.className}">${due.label}</span>
      <div class="task-actions"><button class="action-button" data-action="edit" data-id="${this.escape(id)}" type="button" aria-label="Edit ${this.escape(title)}">✎</button><button class="action-button delete" data-action="delete" data-id="${this.escape(id)}" type="button" aria-label="Hapus ${this.escape(title)}">×</button></div>
    </article>`;
  }

  renderStats() {
    const active = this.tasks.filter(({ completed }) => !completed);
    this.elements.activeCount.textContent = active.length;
    this.elements.doneCount.textContent = this.tasks.filter(({ completed }) => completed).length;
    this.elements.urgentCount.textContent = active.filter(({ priority }) => priority === "high").length;
  }

  renderAgenda() {
    const upcoming = [...this.tasks].filter(({ completed, dueDate }) => !completed && this.isWithinNextWeek(new Date(`${dueDate}T00:00:00`))).sort((a, b) => a.dueDate.localeCompare(b.dueDate)).slice(0, 4);
    const rows = upcoming.length ? upcoming : this.tasks.filter(({ completed }) => !completed).slice(0, 4);
    document.querySelector("#week-agenda").innerHTML = rows.length ? rows.map((task) => {
      const date = new Date(`${task.dueDate}T00:00:00`);
      const isToday = this.toDateInput(new Date()) === task.dueDate;
      return `<div class="agenda-row ${isToday ? "today" : ""}"><div class="agenda-date"><strong>${date.getDate()}</strong><span>${date.toLocaleDateString("id-ID", { month: "short" }).toUpperCase()}</span></div><div class="agenda-info"><strong>${this.escape(task.title)}</strong><span>${this.escape(task.course)} · ${this.priorityLabel(task.priority)}</span></div></div>`;
    }).join("") : `<div class="empty-agenda">Belum ada agenda mendatang.</div>`;
  }

  openDialog(task = null) {
    this.editingId = task?.id || null;
    this.elements.dialogTitle.textContent = task ? "Edit tugas" : "Tambah tugas";
    this.elements.taskId.value = task?.id || "";
    this.elements.title.value = task?.title || "";
    this.elements.course.value = task?.course || "";
    this.elements.dueDate.value = task?.dueDate || this.toDateInput(new Date());
    this.elements.priority.value = task?.priority || "medium";
    this.elements.note.value = task?.note || "";
    this.clearErrors();
    this.elements.dialog.showModal();
    setTimeout(() => this.elements.title.focus(), 50);
  }

  handleSubmit(event) {
    event.preventDefault();
    const { title, course, dueDate, priority, note } = this.elements;
    this.clearErrors();
    if (title.value.trim().length < 3) { this.elements.titleError.textContent = "Nama tugas minimal 3 karakter."; title.focus(); return; }
    if (!dueDate.value) { this.elements.dueError.textContent = "Deadline wajib diisi."; dueDate.focus(); return; }
    const payload = { title: title.value.trim(), course: course.value.trim() || "Umum", dueDate: dueDate.value, priority: priority.value, note: note.value.trim() };
    if (this.editingId) {
      this.tasks = this.tasks.map((task) => task.id === this.editingId ? new TaskItem({ ...task, ...payload }) : task);
      this.showToast("Tugas berhasil diperbarui.");
    } else {
      this.tasks = [...this.tasks, new TaskItem(payload)];
      this.showToast("Tugas baru berhasil ditambahkan.");
    }
    this.saveTasks(); this.renderAll(); this.elements.dialog.close();
  }

  handleTaskAction(event) {
    const button = event.target.closest("[data-action]");
    if (!button) return;
    const task = this.tasks.find(({ id }) => id === button.dataset.id);
    if (!task) return;
    if (button.dataset.action === "edit") this.openDialog(task);
    if (button.dataset.action === "delete") this.deleteTask(task.id);
  }

  toggleTask(id) {
    this.tasks = this.tasks.map((task) => task.id === id ? new TaskItem({ ...task.toJSON(), completed: !task.completed }) : task);
    this.saveTasks(); this.renderAll();
  }

  deleteTask(id) {
    const task = this.tasks.find(({ id: taskId }) => taskId === id);
    if (!task || !window.confirm(`Hapus tugas “${task.title}”?`)) return;
    this.tasks = this.tasks.filter(({ id: taskId }) => taskId !== id);
    this.saveTasks(); this.renderAll(); this.showToast("Tugas dihapus.");
  }

  clearErrors() { this.elements.titleError.textContent = ""; this.elements.dueError.textContent = ""; }
  showToast(message) { const { toast } = this.elements; toast.textContent = message; toast.classList.add("show"); clearTimeout(this.quoteTimer); this.quoteTimer = setTimeout(() => toast.classList.remove("show"), 2600); }
  priorityLabel(priority) { return ({ high: "Tinggi", medium: "Sedang", low: "Rendah" })[priority] || "Sedang"; }
  toDateInput(date) { return date.toISOString().slice(0, 10); }

  isWithinNextWeek(date) { const today = new Date(); today.setHours(0, 0, 0, 0); const limit = new Date(today); limit.setDate(today.getDate() + 7); return date >= today && date <= limit; }
  formatDueDate(value) { const today = this.toDateInput(new Date()); const date = new Date(`${value}T00:00:00`); const diff = Math.ceil((date - new Date(`${today}T00:00:00`)) / 86400000); if (diff === 0) return { label: "Hari ini", className: "today" }; if (diff === 1) return { label: "Besok", className: "today" }; if (diff < 0) return { label: "Terlewat", className: "overdue" }; return { label: date.toLocaleDateString("id-ID", { day: "numeric", month: "short" }), className: "" }; }
  escape(value) { return String(value).replace(/[&<>'"]/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#039;", '"': "&quot;" }[character])); }
}

new DashboardApp();
