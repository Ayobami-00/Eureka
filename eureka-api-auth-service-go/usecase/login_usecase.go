package usecase

import (
	"context"

	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/domain"
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/repository"
)

type loginUsecase struct {
	userRepository repository.UserRepository
}

type LoginUsecase interface {
	Create(ctx context.Context, user *domain.User) error
	GetUserByEmail(ctx context.Context, email string) (domain.User, error)
}

func NewLoginUsecase(userRepository repository.UserRepository) LoginUsecase {
	return &loginUsecase{
		userRepository: userRepository,
	}
}

func (ru *loginUsecase) Create(ctx context.Context, user *domain.User) error {
	return ru.userRepository.Create(ctx, user)
}

func (ru *loginUsecase) GetUserByEmail(ctx context.Context, email string) (domain.User, error) {
	return ru.userRepository.GetByEmail(ctx, email)
}
