import axios from "axios";

import { get } from "svelte/store";
import { access_token, user_id, is_login } from "@/lib/store";

const api_url = import.meta.env.VITE_API_URL;
const api_port = import.meta.env.VITE_API_PORT;
const api = api_url + (api_port === "" ? "" : ":" + api_port);

// Sign
const sign_in = async (stu_id: string, password: string): Promise<boolean> => {
    let frm = new FormData();

    frm.append("stu_id", stu_id);
    frm.append("password", password);

    try {
        const res = await axios.post(api + "/users/login/", frm, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });

        if (res.data.token !== null && res.data.token !== undefined) {
            access_token.set(res.data.token);
            is_login.set(true);
            user_id.set(stu_id);
            return true;
        }
    } catch (err) {
        console.log(err);
    }

    return false;
};
const sign_out = async () => {
    try {
        await axios
            .delete(api + "/users/logout/", {
                headers: {
                    Authorization: "Token " + get(access_token),
                },
            })
            .then((res) => {
                access_token.set("");
                is_login.set(false);
                user_id.set("");
                console.log(res.data);
            })
            .catch((err) => {
                console.log(err);
            });
    } catch (err) {
        console.log(err);
    }
};
const sign_up = async (
    stu_id: string,
    first_name: string,
    last_name: string,
    password: string,
    password2: string
) => {
    let frm = new FormData();

    frm.append("stu_id", stu_id);
    frm.append("first_name", first_name);
    frm.append("last_name", last_name);
    frm.append("password", password);
    frm.append("password2", password2);

    await axios
        .post(api + "/users/register/", frm, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        })
        .then((res) => {
            console.log(res.data);
        })
        .catch((err) => {
            console.log(err);
        });
};

// Mypage
const get_my_info = async () => {
    await axios
        .get(api + "/users/user/" + get(user_id), {
            headers: {
                Authorization: get(access_token),
            },
        })
        .then((res) => {
            console.log(res);
        })
        .catch((err) => {
            console.log(err);
        });
};

// Contents
const get_contents = async (contents_id: string): Promise<any> => {
    try {
        const res = await axios.get(api + `/posts/categories/${contents_id}/`);

        if (res.data !== null && res.data !== undefined) {
            return res.data;
        }
    } catch (err) {
        console.log(err);
    }

    return null;
};

// Content
const get_content = async (content_id: string): Promise<any> => {
    try {
        const res = await axios.get(api + `/posts/posts/${content_id}/`);

        if (res.data !== null && res.data !== undefined) {
            return res.data;
        }
    } catch (err) {
        return null;
    }

    return null;
};

export { sign_in, sign_up, sign_out, get_my_info, get_contents, get_content };
