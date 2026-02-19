/**
 * User model
 */

const users = []; // In-memory storage for demo
let nextId = 1;

class User {
  constructor({ id, name, email, password, createdAt }) {
    this.id = id || nextId++;
    this.name = name;
    this.email = email;
    this.password = password; // TODO: Hash passwords
    this.createdAt = createdAt || new Date();
  }

  static async findAll() {
    return users.map(u => ({ id: u.id, name: u.name, email: u.email }));
  }

  static async findById(id) {
    return users.find(u => u.id === parseInt(id));
  }

  static async findByEmail(email) {
    return users.find(u => u.email === email);
  }

  static async create(data) {
    const user = new User(data);
    users.push(user);
    return user;
  }

  static async deleteById(id) {
    const index = users.findIndex(u => u.id === parseInt(id));
    if (index !== -1) {
      users.splice(index, 1);
    }
  }

  async save() {
    const index = users.findIndex(u => u.id === this.id);
    if (index !== -1) {
      users[index] = this;
    }
    return this;
  }

  toJSON() {
    return {
      id: this.id,
      name: this.name,
      email: this.email,
      createdAt: this.createdAt
    };
  }
}

module.exports = User;
