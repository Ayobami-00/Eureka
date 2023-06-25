package gapi

import (
	"context"
	"fmt"
	"time"

	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/repository"
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/utils/api_response"

	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/pb"
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/utils/validator"
)

func (s *Server) RenewToken(ctx context.Context, req *pb.RenewTokenRequest) (*pb.RenewTokenResponse, error) {

	err := validator.ValidateRenewTokenRequest(req)
	if err != nil {
		return api_response.ErrorBadRequest(&pb.RenewTokenResponse{}, err.Error()).(*pb.RenewTokenResponse), nil
	}

	refreshPayload, err := s.TokenMaker.VerifyToken(
		req.RefreshToken,
	)

	if err != nil {
		return api_response.ErrorInternal(&pb.RenewTokenResponse{}, fmt.Sprintf("Failed to verify token: %s", err)).(*pb.RenewTokenResponse), nil
	}

	sr := repository.NewSessionRepository(s.Db, s.Timeout, s.Db.SessionsTableName)

	session, err := sr.GetByID(ctx, refreshPayload.ID.String())

	if err != nil {
		return api_response.ErrorInternal(&pb.RenewTokenResponse{}, err.Error()).(*pb.RenewTokenResponse), nil
	}

	if session.IsBlocked {

		return api_response.ErrorUnauthorized(&pb.RenewTokenResponse{}, fmt.Sprintf("Blocked session: %s", err)).(*pb.RenewTokenResponse), nil
	}

	if session.Name != string(refreshPayload.Username) {

		return api_response.ErrorUnauthorized(&pb.RenewTokenResponse{}, fmt.Sprintf("Incorrect session user: %s", err)).(*pb.RenewTokenResponse), nil
	}

	if session.RefreshToken != string(req.RefreshToken) {

		return api_response.ErrorUnauthorized(&pb.RenewTokenResponse{}, fmt.Sprintf("Mismatched session token: %s", err)).(*pb.RenewTokenResponse), nil
	}

	if time.Now().After(time.Unix(session.ExpiresAt, 0)) {

		return api_response.ErrorUnauthorized(&pb.RenewTokenResponse{}, fmt.Sprintf("Expired session: %s", err)).(*pb.RenewTokenResponse), nil
	}

	accessToken, accessPayload, err := s.TokenMaker.CreateToken(
		refreshPayload.Username,
		s.Env.AccessTokenDuration,
	)

	if err != nil {
		return api_response.ErrorInternal(&pb.RenewTokenResponse{}, fmt.Sprintf("Failed to generate access token: %s", err)).(*pb.RenewTokenResponse), nil
	}

	return api_response.Success(&pb.RenewTokenResponse{}, "User token refreshed successfully", map[string]interface{}{
		"access_token":            accessToken,
		"access_token_expires_at": accessPayload.ExpiredAt.Unix(),
	}).(*pb.RenewTokenResponse), nil

}
