package api_response

import (
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/pb"
	"google.golang.org/grpc/codes"
)

type ApiResponse interface {
	Success(message string, args map[string]interface{}) interface{}
	ErrorInternal(message string) interface{}
	ErrorBadRequest(message string) interface{}
	ErrorNotFound(message string) interface{}
	ErrorAlreadyExists(message string) interface{}
}

func Success(response interface{}, message string, args map[string]interface{}) interface{} {

	switch r := response.(type) {

	case *pb.RegisterResponse:

		rr := r
		rr.Code = int64(codes.OK)
		rr.Message = message
		return rr

	case *pb.LoginResponse:

		rr := r
		rr.Code = int64(codes.OK)
		rr.Message = message
		rr.SessionId = args["session_id"].(string)
		rr.AccessToken = args["access_token"].(string)
		rr.AccessTokenExpiresAt = args["access_token_expires_at"].(int64)
		rr.RefreshToken = args["refresh_token"].(string)
		rr.RefreshTokenExpiresAt = args["refresh_token_expires_at"].(int64)
		rr.UserId = args["user_id"].(string)
		return rr

	case *pb.ValidateResponse:

		rr := r
		rr.Code = int64(codes.OK)
		rr.Message = message
		rr.UserId = args["user_id"].(string)
		return rr

	case *pb.RenewTokenResponse:

		rr := r
		rr.Code = int64(codes.OK)
		rr.Message = message
		rr.AccessToken = args["access_token"].(string)
		rr.AccessTokenExpiresAt = args["access_token_expires_at"].(int64)
		return rr

	default:

		return nil

	}
}

func ErrorInternal(response interface{}, message string) interface{} {

	switch r := response.(type) {

	case *pb.RegisterResponse:

		rr := r
		rr.Code = int64(codes.Internal)
		rr.Message = message
		return rr

	case *pb.LoginResponse:

		rr := r
		rr.Code = int64(codes.Internal)
		rr.Message = message
		return rr

	case *pb.ValidateResponse:

		rr := r
		rr.Code = int64(codes.Internal)
		rr.Message = message
		return rr

	case *pb.RenewTokenResponse:

		rr := r
		rr.Code = int64(codes.Internal)
		rr.Message = message
		return rr

	default:

		return nil

	}
}

func ErrorBadRequest(response interface{}, message string) interface{} {

	switch r := response.(type) {

	case *pb.RegisterResponse:

		rr := r
		rr.Code = int64(codes.InvalidArgument)
		rr.Message = message
		return rr

	case *pb.LoginResponse:

		rr := r
		rr.Code = int64(codes.InvalidArgument)
		rr.Message = message
		return rr

	case *pb.ValidateResponse:

		rr := r
		rr.Code = int64(codes.InvalidArgument)
		rr.Message = message
		return rr

	case *pb.RenewTokenResponse:

		rr := r
		rr.Code = int64(codes.InvalidArgument)
		rr.Message = message
		return rr

	default:

		return nil

	}
}

func ErrorNotFound(response interface{}, message string) interface{} {

	switch r := response.(type) {

	case *pb.RegisterResponse:

		rr := r
		rr.Code = int64(codes.NotFound)
		rr.Message = message
		return rr

	case *pb.LoginResponse:

		rr := r
		rr.Code = int64(codes.NotFound)
		rr.Message = message
		return rr

	case *pb.ValidateResponse:

		rr := r
		rr.Code = int64(codes.NotFound)
		rr.Message = message
		return rr

	case *pb.RenewTokenResponse:

		rr := r
		rr.Code = int64(codes.NotFound)
		rr.Message = message
		return rr

	default:

		return nil

	}
}

func ErrorAlreadyExists(response interface{}, message string) interface{} {

	switch r := response.(type) {

	case *pb.RegisterResponse:

		rr := r
		rr.Code = int64(codes.AlreadyExists)
		rr.Message = message
		return rr

	case *pb.LoginResponse:

		rr := r
		rr.Code = int64(codes.AlreadyExists)
		rr.Message = message
		return rr

	case *pb.ValidateResponse:

		rr := r
		rr.Code = int64(codes.AlreadyExists)
		rr.Message = message
		return rr

	case *pb.RenewTokenResponse:

		rr := r
		rr.Code = int64(codes.AlreadyExists)
		rr.Message = message
		return rr

	default:

		return nil

	}
}

func ErrorUnauthorized(response interface{}, message string) interface{} {

	switch r := response.(type) {

	case *pb.RegisterResponse:

		rr := r
		rr.Code = int64(codes.PermissionDenied)
		rr.Message = message
		return rr

	case *pb.LoginResponse:

		rr := r
		rr.Code = int64(codes.PermissionDenied)
		rr.Message = message
		return rr

	case *pb.ValidateResponse:

		rr := r
		rr.Code = int64(codes.PermissionDenied)
		rr.Message = message
		return rr

	case *pb.RenewTokenResponse:

		rr := r
		rr.Code = int64(codes.PermissionDenied)
		rr.Message = message
		return rr

	default:

		return nil

	}
}
