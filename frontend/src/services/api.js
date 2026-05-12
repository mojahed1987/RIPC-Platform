export async function getRestrictions() {
  const response = await fetch("http://127.0.0.1:8000/restrictions");
  return response.json();
}