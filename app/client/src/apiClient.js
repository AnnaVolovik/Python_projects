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

    submitSeleniumPage() {
        return this.perform('get', '/project_two')
    }

    submitAioHttpPage() {
        return this.perform('get', '/project_three')
    }

    getPandasDataFrame() {
        return this.perform('get', '/get_entire_df')
    }

    getOnlyGoldResults() {
        return this.perform('get', '/get_only_gold')
    }

    getTreeLikeContent() {
        console.log('hhh')
        return this.perform('get', '/get_tree_like_content')
    }
    restructureTreeLikeData() {
        return this.perform('get', '/restructure_tree_like_data')
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


