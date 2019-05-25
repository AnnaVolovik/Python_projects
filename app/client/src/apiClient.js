import axios from 'axios';

const BASE_URI = 'http://localhost:5000';

const client = axios.create({
  baseURL: BASE_URI,
  json: true
});

export default class APIClient {

    // project one methods
    addEntryProjectOne(data) {
        return this.perform('post', '/page_1', data)
    }

    showEntriesProjectOne() {
        return this.perform('get', '/page_2')
    }

    getPandasDataFrame() {
        return this.perform('get', '/project_five')
    }

    async perform(method, resource, data) {
        return client({
            method,
            url:resource,
            data
        }).then(resp => {
            return resp.data ? resp.data : []
        })
    }

}


