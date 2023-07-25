/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { api__endpoints__v1__auth__User } from "../models/api__endpoints__v1__auth__User";
import type { Body_create_session_v1_session_post } from "../models/Body_create_session_v1_session_post";
import type { Body_login_for_access_token_v1_auth_token_post } from "../models/Body_login_for_access_token_v1_auth_token_post";
import type { Movie } from "../models/Movie";
import type { Session } from "../models/Session";
import type { SessionMatches } from "../models/SessionMatches";
import type { Token } from "../models/Token";
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
  public static loginV1AuthLoginPost(): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/v1/auth/login",
    });
  }

  /**
   * Login For Access Token
   * @param formData
   * @returns Token Successful Response
   * @throws ApiError
   */
  public static loginForAccessTokenV1AuthTokenPost(
    formData: Body_login_for_access_token_v1_auth_token_post,
  ): CancelablePromise<Token> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/v1/auth/token",
      formData: formData,
      mediaType: "application/x-www-form-urlencoded",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Read Users Me
   * @returns api__endpoints__v1__auth__User Successful Response
   * @throws ApiError
   */
  public static readUsersMeV1AuthUsersMeGet(): CancelablePromise<api__endpoints__v1__auth__User> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/v1/auth/users/me/",
    });
  }

  /**
   * Read Own Items
   * @returns any Successful Response
   * @throws ApiError
   */
  public static readOwnItemsV1AuthUsersMeItemsGet(): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/v1/auth/users/me/items/",
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
   * @param sessionId
   * @returns Movie Successful Response
   * @throws ApiError
   */
  public static getNextMovieV1SessionSessionIdNextMovieGet(
    sessionId: string,
  ): CancelablePromise<Movie> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/v1/session/{session_id}/next_movie",
      path: {
        session_id: sessionId,
      },
      errors: {
        422: `Validation Error`,
      },
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
