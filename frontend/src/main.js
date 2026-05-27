import { createApp, onMounted, ref } from "vue";
import * as echarts from "echarts";
import "./style.css";

const App = {
  setup() {
    const dashboard = ref(null);
    onMounted(async () => {
      const response = await fetch("/api/dashboard");
      dashboard.value = await response.json();
      const chart = echarts.init(document.getElementById("theme-chart"));
      chart.setOption({
        xAxis: { type: "category", data: dashboard.value.themes.map((item) => item.name) },
        yAxis: { type: "value" },
        series: [{ type: "bar", data: dashboard.value.themes.map((item) => item.score) }],
      });
    });
    return { dashboard };
  },
  template: `
    <main>
      <header>
        <h1>Monster Quant</h1>
        <p v-if="dashboard">情绪：{{ dashboard.emotion.stage }} / 风险：{{ dashboard.emotion.risk_level }}</p>
      </header>
      <section id="theme-chart"></section>
      <section v-if="dashboard">
        <h2>TOP10 妖股池</h2>
        <table>
          <thead><tr><th>代码</th><th>名称</th><th>主线</th><th>分数</th><th>理由</th></tr></thead>
          <tbody>
            <tr v-for="item in dashboard.monsters" :key="item.code">
              <td>{{ item.code }}</td><td>{{ item.name }}</td><td>{{ item.theme }}</td>
              <td>{{ item.total }}</td><td>{{ item.reasons.join("、") }}</td>
            </tr>
          </tbody>
        </table>
      </section>
    </main>
  `,
};

createApp(App).mount("#app");
