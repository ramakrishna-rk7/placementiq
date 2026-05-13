import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:18081';

export async function askQuestion(question) {
  const { data } = await axios.post(`${API_BASE}/query`, { question });
  return data;
}

export async function uploadDocument({ file, company, round_type, topic, year }) {
  const form = new FormData();
  form.append('file', file);
  form.append('company', company);
  form.append('round_type', round_type);
  form.append('topic', topic);
  form.append('year', year);
  const { data } = await axios.post(`${API_BASE}/documents/upload`, form);
  return data;
}

export async function getRepeatedTopics() {
  const { data } = await axios.get(`${API_BASE}/analytics/repeated-topics`);
  return data;
}
