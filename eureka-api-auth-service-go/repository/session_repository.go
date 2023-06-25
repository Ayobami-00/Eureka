package repository

import (
	"context"
	"fmt"
	"time"

	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/bootstrap"
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/domain"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
)

type sessionRepository struct {
	Db        bootstrap.Database
	TableName string
	Timeout   time.Duration
}

type SessionRepository interface {
	Create(ctx context.Context, session *domain.Session) error
	Fetch(ctx context.Context) ([]domain.Session, error)
	GetByID(ctx context.Context, id string) (domain.Session, error)
}

func NewSessionRepository(db bootstrap.Database, timeout time.Duration, tableName string) SessionRepository {
	return &sessionRepository{
		Db:        db,
		TableName: tableName,
		Timeout:   timeout,
	}
}

func (sr *sessionRepository) Create(ctx context.Context, session *domain.Session) error {

	ctx, cancel := context.WithTimeout(ctx, sr.Timeout)
	defer cancel()

	item, err := dynamodbattribute.MarshalMap(session)

	if err != nil {
		return err
	}

	input := &dynamodb.PutItemInput{
		TableName: aws.String(sr.TableName),
		Item:      item,
		ExpressionAttributeNames: map[string]*string{
			"#id": aws.String("id"),
		},
		ConditionExpression: aws.String("attribute_not_exists(#id)"),
	}

	if _, err := sr.Db.Client.PutItemWithContext(ctx, input); err != nil {

		if _, ok := err.(*dynamodb.ConditionalCheckFailedException); ok {
			return err
		}

		return err
	}

	return nil

}

func (sr *sessionRepository) Fetch(ctx context.Context) ([]domain.Session, error) {

	ctx, cancel := context.WithTimeout(ctx, sr.Timeout)
	defer cancel()

	input := &dynamodb.ScanInput{
		TableName: aws.String(sr.TableName),
	}

	res, err := sr.Db.Client.ScanWithContext(ctx, input)

	if err != nil {

		return nil, err
	}

	sessions := []domain.Session{}

	if err := dynamodbattribute.UnmarshalListOfMaps(res.Items, &sessions); err != nil {

		return sessions, err
	}

	return sessions, nil

}

func (sr *sessionRepository) GetByID(ctx context.Context, id string) (domain.Session, error) {

	ctx, cancel := context.WithTimeout(ctx, sr.Timeout)
	defer cancel()

	input := &dynamodb.GetItemInput{
		TableName: aws.String(sr.TableName),
		Key: map[string]*dynamodb.AttributeValue{
			"id": {S: aws.String(id)},
		},
	}

	var session domain.Session

	res, err := sr.Db.Client.GetItemWithContext(ctx, input)

	if err != nil {
		return session, err
	}

	if res.Item == nil {
		return session, err
	}

	fmt.Println(res.Item)

	if err := dynamodbattribute.UnmarshalMap(res.Item, &session); err != nil {

		return session, err
	}

	return session, nil

}
