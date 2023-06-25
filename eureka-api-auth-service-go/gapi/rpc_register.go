package gapi

import (
	"context"
	"fmt"

	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/domain"
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/repository"
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/usecase"
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/utils/api_response"
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/utils/crypto"

	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/pb"
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/utils/validator"
)

func (s *Server) Register(ctx context.Context, req *pb.RegisterRequest) (*pb.RegisterResponse, error) {

	err := validator.ValidateRegisterRequest(req)
	if err != nil {
		return api_response.ErrorBadRequest(&pb.RegisterResponse{}, err.Error()).(*pb.RegisterResponse), nil
	}

	ur := repository.NewUserRepository(s.Db, s.Timeout, s.Db.UsersTableName)
	ru := usecase.NewRegisterUsecase(ur)

	_, err = ru.GetUserByEmail(ctx, req.GetEmail())

	if err == nil {
		return api_response.ErrorAlreadyExists(&pb.RegisterResponse{}, "User already exists with the given email").(*pb.RegisterResponse), nil
	}

	hashedPassword, err := crypto.HashPassword(req.GetPassword())
	if err != nil {
		return api_response.ErrorInternal(&pb.RegisterResponse{}, fmt.Sprintf("Failed to hash password: %s", err)).(*pb.RegisterResponse), nil
	}

	req.Password = hashedPassword

	user := domain.ParseDomainFromReq(req).(domain.User)

	err = ru.Create(ctx, &user)
	if err != nil {
		return api_response.ErrorInternal(&pb.RegisterResponse{}, err.Error()).(*pb.RegisterResponse), nil
	}

	return api_response.Success(&pb.RegisterResponse{}, "User successfully registered", map[string]interface{}{}).(*pb.RegisterResponse), nil

}
