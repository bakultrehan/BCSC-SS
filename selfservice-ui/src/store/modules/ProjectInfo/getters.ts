import { GetterTree } from 'vuex';
import { ProjectInfoState } from './types';
import { RootState } from '../../types';

/**
 * Getters ProjectInfo
 */
export const getters: GetterTree<ProjectInfoState, RootState> = {
  /**
   * isLoading
   * @param {*} state
   * @returns {boolean} - lading status
   */
  isLoading(state) {
    return state.loading;
  },
  /**
   * projectinfo
   * @param {*} state
   * @returns  {object} projectinfo
   */

  getProjectInfoList(state) {
    return state.projectinfoList;
  },
  successStatus(state) {
    return state.successStatus;
  },
  errorStatus(state) {
    return state.errorStatus;
  },
  /**
   * getSingleProjectInfo
   * @param {*} state
   * @returns  {object} projectinfo
   */
  getSingleProjectInfo(state) {
    return state.singleProjectInfo;
  },
  /**
   * getProjectInfoMessage
   * @param {*} state
   * @returns  {object}  projectinfo
   */
  getProjectInfoMessage(state) {
    return state.message;
  },

  getFinalProjectSubmissionStatus(state) {
    return {
      finalErrorStatus: state.finalErrorStatus,
      finalSuccessStatus: state.finalSuccessStatus
    };
  }
};
