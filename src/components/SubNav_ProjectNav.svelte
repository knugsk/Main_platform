<script lang="ts">
    import "./SubNav_PorjectNav.scss";

    import { replace } from "svelte-spa-router";

    const route_list: routeType[] = [
        {name: "프로젝트",  route: "#/contents/project"},
        {name: "구인구직",  route: "#/contents/job"},
        {name: "예산", route: "#/contents/budget"},
    ];
</script>

<div class="menu_a">
    <ul class="menu_a-nav">
        {#each route_list as route_data, index}
            <li class="menu_a-nav-item">
                <a class="menu_a-nav-link" href={route_data.route} on:click={() => replace(route_data.route)}>
                    <span>
                        <div>
                            {route_data.name}
                        </div>
                    </span>
                </a>
            </li>
        {/each}
    </ul>
</div>
