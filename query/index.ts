import axios from "axios";

import { access_token, is_login } from "@/lib/store";

const api_url = import.meta.env.VITE_API_URL;
const api_port = import.meta.env.VITE_API_PORT;
const api = api_url + (api_port === "" ? "" : ":" + api_port);

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

        if (res.data.token !== null || res.data.token !== undefined) {
            access_token.update((token) => res.data.token);
            is_login.update((b) => true);
            return true;
        }
    } catch (err) {
        console.log(err);
    }

    return false;
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

export { sign_in, sign_up };
