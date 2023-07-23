/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_create_session_v1_session_post } from "../models/Body_create_session_v1_session_post";
import type { Movie } from "../models/Movie";
import type { Session } from "../models/Session";
import type { SessionMatches } from "../models/SessionMatches";
import type { Vote } from "../models/Vote";

import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";

export class DefaultService {
  /**
   * Login
   * @returns any Successful Response
   * @throws ApiError
   */
  public static loginV1LoginPost(): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/v1/login",
    });
  }

  /**
   * List Sessions
   * @returns Session Successful Response
   * @throws ApiError
   */
  public static listSessionsV1SessionGet(): CancelablePromise<Array<Session>> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/v1/session",
    });
  }

  /**
   * Create Session
   * @param requestBody
   * @returns Session Successful Response
   * @throws ApiError
   */
  public static createSessionV1SessionPost(
    requestBody: Body_create_session_v1_session_post,
  ): CancelablePromise<Session> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/v1/session",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Session
   * @param sessionId
   * @returns Session Successful Response
   * @throws ApiError
   */
  public static getSessionV1SessionSessionIdGet(
    sessionId: string,
  ): CancelablePromise<Session> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/v1/session/{session_id}",
      path: {
        session_id: sessionId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Join Session
   * @returns Session Successful Response
   * @throws ApiError
   */
  public static joinSessionV1SessionSessionIdJoinGet(): CancelablePromise<Session> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/v1/session/{session_id}/join",
    });
  }

  /**
   * Get Next Movie
   * @returns Movie Successful Response
   * @throws ApiError
   */
  public static getNextMovieV1SessionSessionIdNextMovieGet(): CancelablePromise<Movie> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/v1/session/{session_id}/next_movie",
    });
  }

  /**
   * Vote For Movie
   * @param requestBody
   * @returns string Successful Response
   * @throws ApiError
   */
  public static voteForMovieV1SessionSessionIdMovieMovieIdPost(
    requestBody: Vote,
  ): CancelablePromise<string> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/v1/session/{session_id}/movie/{movie_id}",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Session Matches
   * @returns SessionMatches Successful Response
   * @throws ApiError
   */
  public static getSessionMatchesV1SessionSessionIdMatchesGet(): CancelablePromise<SessionMatches> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/v1/session/{session_id}/matches",
    });
  }
}
