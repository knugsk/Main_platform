<script lang="ts">
  import "./App.scss";

  import Router from "svelte-spa-router";
  import routes from "@routes/index";

  import { sign_out } from "query";
  import { is_login, access_token } from "@/lib/store";

  let checked = false;
  const route_list: routeType[] = [
    {name: "홈",  route: "#/"},
    {name: "공지",  route: "#/contents/notice"},
    {name: "활동",  route: "#/contents/project"},
    {name: "명예의 전당", route: "#/hall_of_fame"},
  ];

  let top4_list: top4Type[]  = [] // {img_url: "", route: ""}

</script>

<div class="container_main wrapper">
  {#if $is_login === true && (window.location.pathname == "/" || window.location.pathname == "/#/")}
    <a class="btn_sign" href="#/" on:click={() => {
        sign_out();
    }}>
        <span>
            <div class="black">
                로그아웃
            </div>
        </span>
    </a>
  {/if}
  <input type="checkbox" id="burger-toggle" bind:checked={checked}>
  <label for="burger-toggle" class="burger-menu">
    <div class="line" />
    <div class="line" />
    <div class="line" />
  </label>
  <div class="menu">
    <div class="menu-inner">
      <ul class="menu-nav">
        {#each route_list as route_data, index}
          <li class="menu-nav-item">
            <a class="menu-nav-link" href={route_data.route} on:click={() => checked = false}>
              <span>
                <div>
                  {route_data.name}
                </div>
              </span>
            </a>
          </li>
        {/each}
      </ul>
      <div class="gallery">
        <div class="title">
          <p>이달의 명예의 전당</p>
        </div>
        <div class="images">
          {#each top4_list as top4, index}
            <a class="image-link" href={top4.route}>
              <div class="image">
                <img src={top4.img_url} alt="" />
              </div>
            </a>
          {/each}
          {#if top4_list.length < 4}
            {#each {length: 4 - top4_list.length} as _, i}
              <div class="image-link">
                <div class="image" />
              </div>
            {/each}
          {/if}
        </div>
      </div>
    </div>
    <img class="knu_logo images" alt="logo" src="logo/knu_logo.jpg" />
  </div>
  <Router {routes} />
</div>