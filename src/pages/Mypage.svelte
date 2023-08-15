<script lang="ts">
    import "./Mypage.scss";

    import { user_id, access_token } from "@/lib/store";
    import { get_my_info } from "query";

    get_my_info();
</script>

<div class="container_mypage">
    <h1>
        마이페이지
    </h1>
</div>